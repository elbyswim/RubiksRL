import numpy as np
from collections import Counter

class Cube:
	def __init__(self):
		self._U = np.array(['W'] * 9).reshape((3, 3))
		self._L = np.array(['O'] * 9).reshape((3, 3))
		self._F = np.array(['G'] * 9).reshape((3, 3))
		self._R = np.array(['R'] * 9).reshape((3, 3))
		self._B = np.array(['B'] * 9).reshape((3, 3))
		self._D = np.array(['Y'] * 9).reshape((3, 3))
		# self._U = np.array([str(i) for i in range(9)], dtype='<U2').reshape((3, 3))
		# self._L = np.array([str(i + 9 * 1) for i in range(9)], dtype='<U2').reshape((3, 3))
		# self._F = np.array([str(i + 9 * 2) for i in range(9)], dtype='<U2').reshape((3, 3))
		# self._R = np.array([str(i + 9 * 3) for i in range(9)], dtype='<U2').reshape((3, 3))
		# self._B = np.array([str(i + 9 * 4) for i in range(9)], dtype='<U2').reshape((3, 3))
		# self._D = np.array([str(i + 9 * 5) for i in range(9)], dtype='<U2').reshape((3, 3))

	def __str__(self):
		return '\n'.join(['  '.join([' ' * 5, ' '.join(self._U[0]), ' ' * 5, ' ' * 5]),
		                  '  '.join([' ' * 5, ' '.join(self._U[1]), ' ' * 5, ' ' * 5]),
		                  '  '.join([' ' * 5, ' '.join(self._U[2]), ' ' * 5, ' ' * 5]),
		                  '  '.join([' '.join(self._L[0]), ' '.join(self._F[0]), ' '.join(self._R[0]), ' '.join(
			                  self._B[0])]),
		                  '  '.join([' '.join(self._L[1]), ' '.join(self._F[1]), ' '.join(self._R[1]), ' '.join(
			                  self._B[1])]),
		                  '  '.join([' '.join(self._L[2]), ' '.join(self._F[2]), ' '.join(self._R[2]), ' '.join(
			                  self._B[2])]),
		                  '  '.join([' ' * 5, ' '.join(self._D[0]), ' ' * 5, ' ' * 5]),
		                  '  '.join([' ' * 5, ' '.join(self._D[1]), ' ' * 5, ' ' * 5]),
		                  '  '.join([' ' * 5, ' '.join(self._D[2]), ' ' * 5, ' ' * 5])]) + '\n'

	def __eq__(self, other):
		return all([(self._U == other._U).all(),
		            (self._L == other._L).all(),
		            (self._F == other._F).all(),
		            (self._R == other._R).all(),
		            (self._B == other._B).all(),
		            (self._D == other._D).all()])

	def solved(self):
		solved = Cube()
		return self == solved

	def U(self):
		self._U = np.rot90(self._U, 3)
		temp = self._L[0].copy(), self._F[0].copy(), self._R[0].copy(), self._B[0].copy()
		self._L[0], self._F[0], self._R[0], self._B[0] = temp[1], temp[2], temp[3], temp[0]

	def L(self):
		self._L = np.rot90(self._L, 3)
		temp = self._U[:, 0].copy(), self._F[:, 0].copy(), self._D[:, 0].copy(), self._B[:, 2].copy()
		self._U[:, 0], self._F[:, 0], self._D[:, 0], self._B[:, 2] = np.flip(temp[3]), temp[0], temp[1], np.flip(temp[2])

	def F(self):
		self._F = np.rot90(self._F, 3)
		temp = self._L[:, 2].copy(), self._U[2].copy(), self._R[:, 0].copy(), self._D[0].copy()
		self._L[:, 2], self._U[2], self._R[:, 0], self._D[0] = temp[3], np.flip(temp[0]), temp[1], np.flip(temp[2])

	def R(self):
		self._R = np.rot90(self._R, 3)
		temp = self._U[:, 2].copy(), self._F[:, 2].copy(), self._D[:, 2].copy(), self._B[:, 0].copy()
		self._U[:, 2], self._F[:, 2], self._D[:, 2], self._B[:, 0] = temp[1], temp[2], np.flip(temp[3]), np.flip(temp[0])

	def B(self):
		self._B = np.rot90(self._B, 3)
		temp = self._L[:, 0].copy(), self._U[0].copy(), self._R[:, 2].copy(), self._D[2].copy()
		self._L[:, 0], self._U[0], self._R[:, 2], self._D[2] = np.flip(temp[1]), temp[2], np.flip(temp[3]), temp[0]

	def D(self):
		self._D = np.rot90(self._D, 3)
		temp = self._L[2].copy(), self._F[2].copy(), self._R[2].copy(), self._B[2].copy()
		self._L[2], self._F[2], self._R[2], self._B[2] = temp[3], temp[0], temp[1], temp[2]
		
	def scramble(self, s):
		moves = s.strip().split(' ')
		for m in moves:
			if m == 'U':
				self.U()
			elif m == 'U2':
				self.U()
				self.U()
			elif m == "U'":
				self.U()
				self.U()
				self.U()
			elif m == 'L':
				self.L()
			elif m == 'L2':
				self.L()
				self.L()
			elif m == "L'":
				self.L()
				self.L()
				self.L()
			elif m == 'F':
				self.F()
			elif m == 'F2':
				self.F()
				self.F()
			elif m == "F'":
				self.F()
				self.F()
				self.F()
			elif m == 'R':
				self.R()
			elif m == 'R2':
				self.R()
				self.R()
			elif m == "R'":
				self.R()
				self.R()
				self.R()
			elif m == 'B':
				self.B()
			elif m == 'B2':
				self.B()
				self.B()
			elif m == "B'":
				self.B()
				self.B()
				self.B()
			elif m == 'D':
				self.D()
			elif m == 'D2':
				self.D()
				self.D()
			elif m == "D'":
				self.D()
				self.D()
				self.D()
