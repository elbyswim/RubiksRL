import numpy as np
from collections import Counter


class Cube:
    def __init__(self):
        self.faces = np.array([[[i] * 3] * 3 for i in range(6)])
        # self.faces = np.array(range(54)).reshape((6, 3, 3))

    # U, L, F, D, R, B

    def __str__(self):
        color_map = 'WOGYRB'
        # color_map = [str(i) for i in range(54)]
        return '\n'.join(['  '.join([' ' * 5, ' '.join(color_map[i] for i in self.faces[0, 0]), ' ' * 5, ' ' * 5]),
                          '  '.join([' ' * 5, ' '.join(color_map[i] for i in self.faces[0, 1]), ' ' * 5, ' ' * 5]),
                          '  '.join([' ' * 5, ' '.join(color_map[i] for i in self.faces[0, 2]), ' ' * 5, ' ' * 5]),
                          '  '.join([' '.join(color_map[i] for i in self.faces[1, 0]),
                                     ' '.join(color_map[i] for i in self.faces[2, 0]),
                                     ' '.join(color_map[i] for i in self.faces[4, 0]),
                                     ' '.join(color_map[i] for i in self.faces[5, 0])]),
                          '  '.join([' '.join(color_map[i] for i in self.faces[1, 1]),
                                     ' '.join(color_map[i] for i in self.faces[2, 1]),
                                     ' '.join(color_map[i] for i in self.faces[4, 1]),
                                     ' '.join(color_map[i] for i in self.faces[5, 1])]),
                          '  '.join([' '.join(color_map[i] for i in self.faces[1, 2]),
                                     ' '.join(color_map[i] for i in self.faces[2, 2]),
                                     ' '.join(color_map[i] for i in self.faces[4, 2]),
                                     ' '.join(color_map[i] for i in self.faces[5, 2])]),
                          '  '.join([' ' * 5, ' '.join(color_map[i] for i in self.faces[3, 0]), ' ' * 5, ' ' * 5]),
                          '  '.join([' ' * 5, ' '.join(color_map[i] for i in self.faces[3, 1]), ' ' * 5, ' ' * 5]),
                          '  '.join(
                              [' ' * 5, ' '.join(color_map[i] for i in self.faces[3, 2]), ' ' * 5, ' ' * 5])]) + '\n'

    def __eq__(self, other):
        return np.array_equal(self.faces, other.faces)

    def solved(self):
        solved = Cube()
        return self == solved

    def do_move(self, m):
        if m not in {'U', 'U2', 'U\'', 'L', 'L2', 'L\'', 'F', 'F2', 'F\'', 'D', 'D2', 'D\'', 'R', 'R2', 'R\'',
                     'B', 'B2', 'B\''}:
            print('Invalid move.')
            return
        if m == 'U':
            self.faces[0] = np.rot90(self.faces[0], 3)
            self.faces[1, 0], \
            self.faces[2, 0], \
            self.faces[4, 0], \
            self.faces[5, 0] = \
                self.faces[2, 0].copy(), \
                self.faces[4, 0].copy(), \
                self.faces[5, 0].copy(), \
                self.faces[1, 0].copy()
        elif m == 'U2':
            self.do_sequence('U U')
        elif m == 'U\'':
            self.do_sequence('U U U')
        elif m == 'L':
            self.faces[1] = np.rot90(self.faces[1], 3)
            self.faces[0, :, 0], \
            self.faces[2, :, 0], \
            self.faces[3, :, 0], \
            self.faces[5, :, 2] = \
                np.flip(self.faces[5, :, 2].copy()), \
                self.faces[0, :, 0].copy(), \
                self.faces[2, :, 0].copy(), \
                np.flip(self.faces[3, :, 0].copy())
        elif m == 'L2':
            self.do_sequence('L L')
        elif m == 'L\'':
            self.do_sequence('L L L')
        elif m == 'F':
            self.faces[2] = np.rot90(self.faces[2], 3)
            self.faces[0, 2], \
            self.faces[1, :, 2], \
            self.faces[3, 0], \
            self.faces[4, :, 0] = \
                np.flip(self.faces[1, :, 2].copy()), \
                self.faces[3, 0].copy(), \
                np.flip(self.faces[4, :, 0].copy()), \
                self.faces[0, 2].copy()
        elif m == 'F2':
            self.do_sequence('F F')
        elif m == 'F\'':
            self.do_sequence('F F F')
        elif m == 'D':
            self.faces[3] = np.rot90(self.faces[3], 3)
            self.faces[1, 2], \
            self.faces[2, 2], \
            self.faces[4, 2], \
            self.faces[5, 2] = \
                self.faces[5, 2].copy(), \
                self.faces[1, 2].copy(), \
                self.faces[2, 2].copy(), \
                self.faces[4, 2].copy()
        elif m == 'D2':
            self.do_sequence('D D')
        elif m == 'D\'':
            self.do_sequence('D D D')
        elif m == 'R':
            self.faces[4] = np.rot90(self.faces[4], 3)
            self.faces[0, :, 2], \
            self.faces[2, :, 2], \
            self.faces[3, :, 2], \
            self.faces[5, :, 0] = \
                self.faces[2, :, 2].copy(), \
                self.faces[3, :, 2].copy(), \
                np.flip(self.faces[5, :, 0].copy()), \
                np.flip(self.faces[0, :, 2].copy())
        elif m == 'R2':
            self.do_sequence('R R')
        elif m == 'R\'':
            self.do_sequence('R R R')
        elif m == 'B':
            self.faces[5] = np.rot90(self.faces[5], 3)
            self.faces[0, 0], \
            self.faces[1, :, 0], \
            self.faces[3, 2], \
            self.faces[4, :, 2] = \
                self.faces[4, :, 2].copy(), \
                np.flip(self.faces[0, 0].copy()), \
                self.faces[1, :, 0].copy(), \
                np.flip(self.faces[3, 2].copy())
        elif m == 'B2':
            self.do_sequence('B B')
        elif m == 'B\'':
            self.do_sequence('B B B')

    def do_sequence(self, s, show=False):
        moves = s.strip().split(' ')
        for m in moves:
            self.do_move(m)
            if show:
                print(self)

    def scramble(self, seed=None, print_scramble=False):
        s = get_scramble(seed=seed)
        if print_scramble:
            print(s)
        self.do_sequence(s)
        print(self)

    def reward1(self):
        return 1 if self.solved() else -1

    def reward2(self):
        if self.solved():
            return 1
        return 1 - sum([sum(self._U == 'W'), sum(self._L == 'O'), sum(self._F == 'G'),
                        sum(self._R == 'R'), sum(self._B == 'B'), sum(self._D == 'Y')]) / 54


def get_scramble(length=None, seed=None):
    moves = np.array([["U", "U2", "U'"],
                      ["L", "L2", "L'"],
                      ["F", "F2", "F'"],
                      ["D", "D2", "D'"],
                      ["R", "R2", "R'"],
                      ["B", "B2", "B'"]])
    weights = np.ones(6) / 6
    scramble = []
    if length is None:
        length = np.random.randint(17, 26)
    if seed is not None:
        np.random.seed(seed)
    for _ in range(length):
        i = np.random.choice(range(6), p=weights)
        j = np.random.choice(range(3))
        scramble.append(moves[i, j])
        weights[i] = 0
        for k in range(6):
            if (k - i) % 3:
                weights[k] = 1
        weights[(i + 3) % 6] = 1 if weights[(i + 3) % 6] > 0 else 0
        weights /= weights.sum()
    return ' '.join(scramble)


cube = Cube()
cube.scramble(seed=1, print_scramble=True)
