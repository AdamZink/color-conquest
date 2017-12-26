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
