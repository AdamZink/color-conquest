import numpy as np

class NeighborhoodUtil(object):

	# layerGrid: the numpy object with a slice of the full grid
	# layerColumn: the center index of the column in layerGrid which is the unit's location
	# n: the number of sections out from the center
	# direction: positive or negative number mapped to 1 or -1 respectively. Defaults to positive
	@classmethod
	def getSectionSum(cls, layerGrid, layerColumn, n, direction=1):
		if (n == 0):
			return layerGrid[layerColumn]

		sectionCenterColumn = layerColumn + ((1 if direction > 0 else -1) * (3**(n-1)))
		sectionEdgeOffset = int(int((3**(n-1)) - 1) / 2)

		sectionLeftColumn = sectionCenterColumn - sectionEdgeOffset
		if (sectionLeftColumn < 0):
			sectionLeftColumn = 0

		sectionRightColumn = sectionCenterColumn + sectionEdgeOffset + 1
		if (sectionRightColumn < 0):
			sectionRightColumn = 0

		#print('[' + str(sectionLeftColumn) + ',' + str(sectionRightColumn) + ')')
		return np.sum(layerGrid[sectionLeftColumn:sectionRightColumn])

	# return the sum of each section in the neighborhood
	# layerGrid: the numpy object with a slice of the full grid
	# layerColumn: the center index of the column in layerGrid which is the unit's location
	# maxN: the highest n away from the center. Defaults to 1
	# values like (dimension, n, direction, sum)
	@classmethod
	def getNeighborhoodSumTuples(cls, layerGrid, layerColumn, maxN=1):
		sectionEncodingOrderTuples = NeighborhoodUtil.getSectionEncodingOrderTuples(maxN)
		neighborhoodSumTuples = []

		for sectionEncodingOrderTuple in sectionEncodingOrderTuples:
			neighborhoodSumTuples.append(
				sectionEncodingOrderTuple +
				(NeighborhoodUtil.getSectionSum(layerGrid, layerColumn, sectionEncodingOrderTuple[1], sectionEncodingOrderTuple[2]),)
			)
		return neighborhoodSumTuples

	# return the normalized sum of each section in the neighborhood
	# layerGrid: the numpy object with a slice of the full grid
	# layerColumn: the center index of the column in layerGrid which is the unit's location
	# maxN: the highest n away from the center. Defaults to 1
	# buckets: the number of divisions to normalize and take ceiling of the sums. Defaults to 2
	# values like (dimension, n, direction, normalized sum bucket)
	@classmethod
	def getNormalizedNeighborhoodSumTuples(cls, layerGrid, layerColumn, maxN=1, buckets=2):
		if (buckets < 2):
			return []

		neighborhoodSumTuples = NeighborhoodUtil.getNeighborhoodSumTuples(layerGrid, layerColumn, maxN)
		largestSum = np.max([t[3] for t in neighborhoodSumTuples])
		normalizedNeighborhoodSumTuples = [
			t[0:3] +
			(0 if largestSum == 0 else int(np.ceil((t[3] / largestSum) * (buckets - 1))),)
			for t in neighborhoodSumTuples
		]

		return normalizedNeighborhoodSumTuples

	# return list with tuples based on the number of dimensions
	# the direction of each tuple is positive
	# assume dimensions equals 1 in current version of simulation
	@classmethod
	def getPositiveDimensionTuples(cls):
		return [(0, 1)]

	# return list with tuples based on the number of dimensions
	# the direction of each tuple is negative
	# assume dimensions equals 1 in current version of simulation
	@classmethod
	def getNegativeDimensionTuples(cls):
		return [(0, -1)]

	# return list of tuples in the order of dimensions to be encoded
	# the first tuple value is the dimension with negative direction
	# the second tuple value is the dimension with positive direction
	@classmethod
	def getDimensionEncodingTuples(cls):
		negativeDimensionTuples = NeighborhoodUtil.getNegativeDimensionTuples()
		positiveDimensionTuples = NeighborhoodUtil.getPositiveDimensionTuples()
		dimensionEncodingTuples = []
		for negativeDimensionTuple in negativeDimensionTuples:
			for positiveDimensionTuple in positiveDimensionTuples:
				dimensionEncodingTuples.append((negativeDimensionTuple, positiveDimensionTuple))
		return dimensionEncodingTuples

	# return list of tuples, e.g. (dimension, n, direction), as the section encoding order
	# maxN: the highest n away from the center. Defaults to 1
	@classmethod
	def getSectionEncodingOrderTuples(cls, maxN=1):
		dimensionEncodingTuples = NeighborhoodUtil.getDimensionEncodingTuples()
		sectionEncodingOrderTuples = [(0, 0, 1)]
		n = 1
		while (n <= maxN):
			for dimensionEncodingTuple in dimensionEncodingTuples:
				for dimensionTuple in dimensionEncodingTuple:
					sectionEncodingOrderTuples.append((dimensionTuple[0], n, dimensionTuple[1]))
			n += 1
		return sectionEncodingOrderTuples

	# return binary value of encoded neighborhood by shifting bits to the left
	# layerGrid: the numpy object with a slice of the full grid
	# layerColumn: the center index of the column in layerGrid which is the unit's location
	# maxN: the highest n away from the center. Defaults to 1
	# buckets: the number of divisions to normalize and take ceiling of the sums. Defaults to 2
	@classmethod
	def getEncodedNeighborhood(cls, layerGrid, layerColumn, maxN=1, buckets=2):
		encodedNeighborhood = 0b0
		normalizedNeighborhoodSumTuples = NeighborhoodUtil.getNormalizedNeighborhoodSumTuples(layerGrid, layerColumn, maxN, buckets)
		bucketBitsNeeded = (buckets - 1).bit_length()
		for normalizedNeighborhoodSumTuple in normalizedNeighborhoodSumTuples:
			encodedNeighborhood = (encodedNeighborhood << bucketBitsNeeded) + normalizedNeighborhoodSumTuple[3]
		return encodedNeighborhood

	# return string description of center of the neighborhood
	@classmethod
	def describeEncodedCenter(cls, encodedCenter):
		if (encodedCenter > 0b0):
			return ['The center has units']
		else:
			return []

	# return string description of section of the neighborhood
	@classmethod
	def describeEncodedSection(cls, encodedSection, dimension, n, direction):
		if (encodedSection > 0b0):
			return ['Dimension ' + str(dimension) + ', Section ' + ('-' if direction < 0 else '+') + str(n) + ' has units']
		else:
			return []

	# return list with string descriptions of encoded neighborhood
	@classmethod
	def describeEncodedNeighborhood(cls, encodedNeighborhood, maxN=1, buckets=2):
		descriptionList = []
		n = maxN
		bucketBitsNeeded = (buckets - 1).bit_length()
		while (n > 0):
			positiveMask = (1 << bucketBitsNeeded) - 1
			descriptionList += NeighborhoodUtil.describeEncodedSection(encodedNeighborhood & positiveMask, 0, n, 1)
			encodedNeighborhood = encodedNeighborhood >> bucketBitsNeeded

			negativeMask = (1 << bucketBitsNeeded) - 1
			descriptionList += NeighborhoodUtil.describeEncodedSection(encodedNeighborhood & negativeMask, 0, n, -1)
			encodedNeighborhood = encodedNeighborhood >> bucketBitsNeeded

			n -= 1

		descriptionList += NeighborhoodUtil.describeEncodedCenter(encodedNeighborhood)
		return descriptionList
