import unittest
from neighborhood_util import NeighborhoodUtil

import numpy as np

class TestNeighborhoodUtil(unittest.TestCase):

	# Tests for getSectionSum
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


	# Tests for getPositiveDimensionTuples
	def test_getPositiveDimensionTuples_1D(self):
		correctTuples1D = [(0, 1)]
		positiveDimensionTuples1D = NeighborhoodUtil.getPositiveDimensionTuples()
		self.assertListEqual(correctTuples1D, positiveDimensionTuples1D)


	# Tests for getNegativeDimensionTuples
	def test_getNegativeDimensionTuples_1D(self):
		correctTuples1D = [(0, -1)]
		negativeDimensionTuples1D = NeighborhoodUtil.getNegativeDimensionTuples()
		self.assertListEqual(correctTuples1D, negativeDimensionTuples1D)


	# Tests for getDimensionEncodingTuples
	def test_getDimensionEncodingTuples_1D(self):
		correctTuples1D = [((0, -1), (0, 1))]
		dimensionEncodingTuples1D = NeighborhoodUtil.getDimensionEncodingTuples()
		self.assertListEqual(correctTuples1D, dimensionEncodingTuples1D)


	# Tests for getSectionEncodingOrderTuples
	# tuples like (dimension, n, direction)
	def test_getSectionEncodingOrderTuples_1D_1(self):
		correctTuples1D = [(0, 0, 1), (0, 1, -1), (0, 1, 1)]
		sectionEncodingOrderTuples1D = NeighborhoodUtil.getSectionEncodingOrderTuples(1)
		self.assertListEqual(correctTuples1D, sectionEncodingOrderTuples1D)

	def test_getSectionEncodingOrderTuples_1D_2(self):
		correctTuples1D = [(0, 0, 1), (0, 1, -1), (0, 1, 1), (0, 2, -1), (0, 2, 1)]
		sectionEncodingOrderTuples1D = NeighborhoodUtil.getSectionEncodingOrderTuples(2)
		self.assertListEqual(correctTuples1D, sectionEncodingOrderTuples1D)


	# Tests for getNeighborhoodSumTuples
	def test_getNeighborhoodSumTuples_1D_0(self):
		correctTuples1D = [(0, 0, 1, 5)]
		layerGrid = np.array([2, 5, 8])
		neighborhoodSumTuples = NeighborhoodUtil.getNeighborhoodSumTuples(layerGrid, 1, 0)
		self.assertListEqual(correctTuples1D, neighborhoodSumTuples)

	def test_getNeighborhoodSumTuples_1D_1(self):
		correctTuples1D = [(0, 0, 1, 5), (0, 1, -1, 2), (0, 1, 1, 8)]
		layerGrid = np.array([2, 5, 8])
		neighborhoodSumTuples = NeighborhoodUtil.getNeighborhoodSumTuples(layerGrid, 1, 1)
		self.assertListEqual(correctTuples1D, neighborhoodSumTuples)


	# Tests for getNormalizedNeighborhoodSumTuples
	def test_getNormalizedNeighborhoodSumTuples_1D_0(self):
		correctTuples1D = [(0, 0, 1, 1)]
		layerGrid = np.array([0, 5, 10])
		neighborhoodSumTuples = NeighborhoodUtil.getNormalizedNeighborhoodSumTuples(layerGrid, 1, 0)
		self.assertListEqual(correctTuples1D, neighborhoodSumTuples)

	def test_getNormalizedNeighborhoodSumTuples_1D_1(self):
		correctTuples1D = [(0, 0, 1, 1), (0, 1, -1, 0), (0, 1, 1, 1)]
		layerGrid = np.array([0, 2, 10])
		neighborhoodSumTuples = NeighborhoodUtil.getNormalizedNeighborhoodSumTuples(layerGrid, 1, 1)
		self.assertListEqual(correctTuples1D, neighborhoodSumTuples)

	def test_getNormalizedNeighborhoodSumTuples_1D_1_with_3_buckets(self):
		correctTuples1D = [(0, 0, 1, 1), (0, 1, -1, 0), (0, 1, 1, 2)]
		layerGrid = np.array([0, 2, 10])
		neighborhoodSumTuples = NeighborhoodUtil.getNormalizedNeighborhoodSumTuples(layerGrid, 1, 1, 3)
		self.assertListEqual(correctTuples1D, neighborhoodSumTuples)


	# Tests for getEncodedNeighborhood
	def test_getEncodedNeighborhood_1D_0_with_2_buckets(self):
		correctEncoding = 0b01
		layerGrid = np.array([0, 5, 10])
		encodedNeighborhood = NeighborhoodUtil.getEncodedNeighborhood(layerGrid, 1, 0, 2)
		self.assertEqual(correctEncoding, encodedNeighborhood)

	def test_getEncodedNeighborhood_1D_1_with_2_buckets(self):
		correctEncoding = 0b010001
		layerGrid = np.array([0, 5, 10])
		encodedNeighborhood = NeighborhoodUtil.getEncodedNeighborhood(layerGrid, 1, 1, 2)
		self.assertEqual(correctEncoding, encodedNeighborhood)

	def test_getEncodedNeighborhood_1D_1_with_4_buckets(self):
		correctEncoding = 0b100111
		layerGrid = np.array([2, 5, 10])
		encodedNeighborhood = NeighborhoodUtil.getEncodedNeighborhood(layerGrid, 1, 1, 4)
		self.assertEqual(correctEncoding, encodedNeighborhood)

	def test_getEncodedNeighborhood_1D_10_all_zeros_with_2_buckets(self):
		correctEncoding = 0b0
		layerGrid = np.array([0])
		encodedNeighborhood = NeighborhoodUtil.getEncodedNeighborhood(layerGrid, 0, 10, 2)
		self.assertEqual(correctEncoding, encodedNeighborhood)


	# Tests for describeEncodedSection
	def test_describeEncodedSection_positive_has_units(self):
		encodedNeighborhood = 0b01
		correctDescriptionList = ['Dimension 0, Section +1 has units']
		descriptionList = NeighborhoodUtil.describeEncodedSection(encodedNeighborhood, 0, 1, 1)
		self.assertEqual(correctDescriptionList, descriptionList)

	def test_describeEncodedSection_negative_has_no_units(self):
		encodedNeighborhood = 0b00
		correctDescriptionList = []
		descriptionList = NeighborhoodUtil.describeEncodedSection(encodedNeighborhood, 0, 1, -1)
		self.assertEqual(correctDescriptionList, descriptionList)


	# Tests for describeEncodedNeighborhood
	def test_describeEncodedNeighborhood_0_has_units(self):
		encodedNeighborhood = 0b1
		correctDescriptionList = ['The center has units']
		descriptionList = NeighborhoodUtil.describeEncodedNeighborhood(encodedNeighborhood, 0, 2)
		self.assertListEqual(correctDescriptionList, descriptionList)

	def test_describeEncodedNeighborhood_0_no_units(self):
		encodedNeighborhood = 0b0
		correctDescriptionList = []
		descriptionList = NeighborhoodUtil.describeEncodedNeighborhood(encodedNeighborhood, 0, 2)
		self.assertListEqual(correctDescriptionList, descriptionList)

	def test_describeEncodedNeighborhood_1_has_units(self):
		encodedNeighborhood = 0b010011
		correctDescriptionList = [
			'Dimension 0, Section +1 has units',
			'The center has units'
		]
		descriptionList = NeighborhoodUtil.describeEncodedNeighborhood(encodedNeighborhood, 1, 4)
		self.assertListEqual(correctDescriptionList, descriptionList)


if __name__ == '__main__':
	unittest.main()
