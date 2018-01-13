from neighborhood_util import NeighborhoodUtil as nutil
import numpy as np

class GridUtil(object):

	# return the 1D array with sum of the opposing units
	# grid: the numpy grid
	# hueIndex: the index of the hue in grid
	@classmethod
	def getGridOpposingSum(cls, grid, hueIndex):
		opposingIndexes = [i for i in range(grid.shape[0]) if i != hueIndex]
		return np.sum(grid.take(opposingIndexes, axis=0), axis=0)

	# return the encoded neighborhood for the sum of the other layers
	# (i.e. all opposing hues flattened to 1 opposing layer)
	# grid: the numpy grid
	# hueIndex: the index of the hue in grid
	# layerColumn: the center column to encode the neighborhood
	# maxN: the number of sections out from the center. Defaults to 1
	# buckets: the number of divisions to normalize and take ceiling of the sums. Defaults to 2
	@classmethod
	def getOpposingEncodedNeighborhood(cls, grid, hueIndex, layerColumn, maxN=1, buckets=2):
		gridOpposingSumLayer = GridUtil.getGridOpposingSum(grid, hueIndex)
		return nutil.getEncodedNeighborhood(gridOpposingSumLayer, layerColumn, maxN, buckets)
