from adi import *

from collections import defaultdict
import tensorflow as tf


def monte_carlo_tree_search(model, cube, c=4, v=2, move_set='QTM', max_moves=100):
    moves = get_moves(move_set)
    num_actions = len(moves)
    state = cube
    state_key = str(state)
    leaves = {state_key}
    seen = set()
    N = defaultdict(lambda: np.zeros(num_actions))
    W = defaultdict(lambda: np.zeros(num_actions))
    L = defaultdict(lambda: np.zeros(num_actions))
    P = {state_key: predict(model, cube)[1][0]}
    solution = []
    path = [state.copy()]
    for _ in range(max_moves):
        if state.solved():
            return True, [moves[a] for a in solution], path
        U = np.zeros(num_actions)
        Q = np.zeros(num_actions)
        for i, move in enumerate(moves):
            U[i] = c * P[state_key][i] * np.sqrt(N[state_key].sum() + 1) / (1 + N[state_key][i])
            Q[i] = W[state_key][i] - L[state_key][i]
        A = np.argmax(U + Q)
        L[state_key][A] += v
        solution.append(A)
        if state_key in leaves:
            leaves.discard(state_key)
            seen.add(state_key)
            for move in moves:
                child = state.copy()
                child.do_move(move)
                child_key = str(child)
                P[child_key] = predict(model, child)[1][0]
                if child_key not in seen:
                    leaves.add(child_key)
            val = predict(model, state)[0][0]
            for s, a in zip(path, solution):
                key = str(s)
                W[key][a] = max(W[key][a], val)
                N[key][a] += 1
                L[key][a] -= v
        state.do_move(moves[A])
        path.append(state.copy())
        state_key = str(state)
    return False, [moves[a] for a in solution], path


def test(model_folder, num_cubes=100, scramble_length=5, mode='QTM', max_moves=100):
    print('Scramble length: {}'.format(scramble_length))
    model = tf.keras.models.load_model(model_folder)
    num_solved = 0
    sol_lengths = []
    for i in range(num_cubes):
        test_cube = Cube()
        test_cube.scramble(scramble_length, None, mode, False, False)
        solved, solution, path = monte_carlo_tree_search(model, test_cube, max_moves=max_moves)
        num_solved += solved
        if solved:
            sol_lengths.append(len(solution))
    print('{}/{} solved. {} solve rate'.format(num_solved, num_cubes, num_solved / num_cubes))
    print('Average solution length: {}'.format(np.array(sol_lengths).mean()))
    return num_solved / num_cubes, np.array(sol_lengths).mean()


def gradual_test(model_folder, num_cubes=100, mode='QTM', max_moves_factor=10):
    rates = []
    lengths = []
    scramble_length = 1
    while True:
        rate, length = test(model_folder, num_cubes, scramble_length, mode, scramble_length * max_moves_factor)
        if rate == 0:
            break
        rates.append(rate)
        lengths.append(length)
        scramble_length += 1
    return rates, lengths
