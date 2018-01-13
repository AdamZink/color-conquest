import unittest
from grid_util import GridUtil as gutil

import numpy as np

class TestGridUtil(unittest.TestCase):

	# Tests for getGridOpposingSum
	def test_getGridOpposingSum_2_layers_zeros(self):
		gridColumns = 3
		grid = np.zeros(shape=(2, gridColumns))
		hueIndex = 0
		np.testing.assert_array_equal(np.array([0, 0, 0]), gutil.getGridOpposingSum(grid, hueIndex))

	def test_getGridOpposingSum_2_layers_fives_1(self):
		gridColumns = 3
		grid = np.zeros(shape=(2, gridColumns))
		grid[1][:] = 5
		hueIndex = 0
		np.testing.assert_array_equal(np.array([5, 5, 5]), gutil.getGridOpposingSum(grid, hueIndex))

	def test_getGridOpposingSum_2_layers_fives_2(self):
		gridColumns = 3
		grid = np.zeros(shape=(2, gridColumns))
		grid[1][:] = 5
		hueIndex = 1
		np.testing.assert_array_equal(np.array([0, 0, 0]), gutil.getGridOpposingSum(grid, hueIndex))

	def test_getGridOpposingSum_3_layers(self):
		gridColumns = 3
		grid = np.zeros(shape=(10, gridColumns))
		grid[1][:] = 5
		grid[2][:] = 6
		hueIndex = 0
		np.testing.assert_array_equal(np.array([11, 11, 11]), gutil.getGridOpposingSum(grid, hueIndex))


	# Tests for getOpposingEncodedNeighborhood
	def test_getOpposingEncodedNeighborhood_2_layers_zeros(self):
		gridColumns = 3
		grid = np.zeros(shape=(2, gridColumns))
		hueIndex = 0
		layerColumn = 1
		maxN = 1
		self.assertEqual(0b000, gutil.getOpposingEncodedNeighborhood(grid, hueIndex, layerColumn, maxN, 2))

	def test_getOpposingEncodedNeighborhood_2_layers_ones(self):
		gridColumns = 3
		grid = np.ones(shape=(2, gridColumns))
		hueIndex = 0
		layerColumn = 1
		maxN = 1
		self.assertEqual(0b111, gutil.getOpposingEncodedNeighborhood(grid, hueIndex, layerColumn, maxN, 2))

	def test_getOpposingEncodedNeighborhood_2_layers_center(self):
		gridColumns = 3
		grid = np.zeros(shape=(2, gridColumns))
		grid[1][1] = 10
		hueIndex = 0
		layerColumn = 1
		maxN = 1
		self.assertEqual(0b100, gutil.getOpposingEncodedNeighborhood(grid, hueIndex, layerColumn, maxN, 2))


if __name__ == '__main__':
	unittest.main()
