from cube import *
from model import *


def autodidactic_iteration(scramble_length=20, num_iterations=1000, move_set='QTM', reward_mode=1, factor=1,
                           learning_rate=0.0005, verbose=0):
    moves = get_moves(move_set)
    num_actions = len(moves)
    model = build_model(num_actions, factor)
    compile_model(model, learning_rate)
    for iteration in range(num_iterations):
        if (iteration + 1) % 50 == 0:
            print('Iteration {}'.format(iteration + 1))
        scramble = get_scramble(scramble_length).split(' ')
        cube = Cube()
        X = []
        for move in scramble:
            cube.do_move(move)
            X.append(cube.copy())
        Y_v = np.zeros(scramble_length)
        Y_p = np.zeros(scramble_length)
        for i, x in enumerate(X):
            dfs = [x.copy() for _ in range(num_actions)]
            v = np.zeros(num_actions)
            for j, a in enumerate(moves):
                dfs[j].do_move(a)
                v[j] = predict(model, dfs[j])[0][0]
            Y_v[i] = np.amax(np.array([dfs[j].reward(reward_mode) for j in range(num_actions)]) + v)
            Y_p[i] = np.argmax(np.array([dfs[j].reward(reward_mode) for j in range(num_actions)]) + v)
        X_as_numpy = np.zeros((scramble_length, 54))
        for i, x in enumerate(X):
            X_as_numpy[i] = x.faces.flatten()
        model.fit(X_as_numpy, {'value': Y_v, 'policy': Y_p},
                  epochs=100,
                  sample_weight=np.array([1 / (i + 1) for i in range(scramble_length)]), verbose=verbose)
    print('Done training.')
    return model


def predict(model, cube):
    return model(np.expand_dims(cube.faces.flatten(), axis=0))
