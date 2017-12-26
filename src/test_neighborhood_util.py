import unittest
from neighborhood_util import NeighborhoodUtil

import numpy as np

class TestNeighborhoodUtil(unittest.TestCase):

	def test_is_0_getSectionSum_0(self):
		layerGrid = np.zeros((3))
		self.assertEqual(0, NeighborhoodUtil.getSectionSum(layerGrid, 1, 0))

	def test_is_1_getSectionSum_0(self):
		layerGrid = np.array([0, 1, 0])
		self.assertEqual(1, NeighborhoodUtil.getSectionSum(layerGrid, 1, 0))

	def test_is_1_getSectionSum_1_left(self):
		layerGrid = np.array([1, 5, 9])
		self.assertEqual(1, NeighborhoodUtil.getSectionSum(layerGrid, 1, 1, -1))

	def test_is_3_getSectionSum_1_right(self):
		layerGrid = np.array([1, 5, 9])
		self.assertEqual(9, NeighborhoodUtil.getSectionSum(layerGrid, 1, 1, 1))

	def test_is_3_getSectionSum_2_left(self):
		layerGrid = np.array([1, 1, 1, 5, 5, 5, 9, 9, 9])
		self.assertEqual(3, NeighborhoodUtil.getSectionSum(layerGrid, 4, 2, -1))

	def test_is_27_getSectionSum_2_right(self):
		layerGrid = np.array([1, 1, 1, 5, 5, 5, 9, 9, 9])
		self.assertEqual(27, NeighborhoodUtil.getSectionSum(layerGrid, 4, 2, 1))

	def test_is_1_getSectionSum_2_left_out(self):
		layerGrid = np.array([1, 5, 5, 5, 9])
		self.assertEqual(1, NeighborhoodUtil.getSectionSum(layerGrid, 2, 2, -1))

	def test_is_9_getSectionSum_2_right_out(self):
		layerGrid = np.array([1, 5, 5, 5, 9])
		self.assertEqual(9, NeighborhoodUtil.getSectionSum(layerGrid, 2, 2, 1))

	def test_is_0_getSectionSum_3_left_all_out(self):
		layerGrid = np.array([1, 5, 5, 5, 9])
		self.assertEqual(0, NeighborhoodUtil.getSectionSum(layerGrid, 2, 3, -1))

	def test_is_0_getSectionSum_3_right_all_out(self):
		layerGrid = np.array([1, 5, 5, 5, 9])
		self.assertEqual(0, NeighborhoodUtil.getSectionSum(layerGrid, 2, 3, 1))

	def test_is_0_getSectionSum_10_left_all_out(self):
		layerGrid = np.array([1, 5, 5, 5, 9])
		self.assertEqual(0, NeighborhoodUtil.getSectionSum(layerGrid, 0, 10, -1))

	def test_is_0_getSectionSum_10_right_all_out(self):
		layerGrid = np.array([1, 5, 5, 5, 9])
		self.assertEqual(0, NeighborhoodUtil.getSectionSum(layerGrid, 4, 10, 1))


if __name__ == '__main__':
	unittest.main()
