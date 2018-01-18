from grid_util import GridUtil as gutil
from neighborhood_util import NeighborhoodUtil as nutil
from grid_1D import *

import numpy as np

gridHueList = [0, 120]
gridColumns = 4
maxN = 2

grid = Grid1D(gridHueList, gridColumns)
grid.grid[0][0][1] = 3
grid.grid[1][3][1] = 3

# layers = np.zeros(shape=(len(gridHueList), gridColumns))
# layers[0][0] = 1
# layers[1][3] = 1

def testGetMoveOffset(descriptionList):
	for description in descriptionList:
		if 'Section +' in description:
			return 1
		elif 'Section -' in description:
			return -1
	return 0


print('\nInitial:')
grid.display()

numRounds = 4
currentRound = 1

while (currentRound <= numRounds):
	nextGrid = Grid1D(gridHueList, gridColumns)
	nextGrid.grid = np.copy(grid.grid[:, :, :])

	for layerColumn in range(gridColumns):
		for hueIndex in range(len(gridHueList)):
			if grid.grid[hueIndex][layerColumn][1] > 0:
				print('\nHue ' + str(grid.hueList[hueIndex]) + ', column index ' + str(layerColumn) + ':')

				print(grid.grid[:, :, 1])
				descriptionList = nutil.describeEncodedNeighborhood(
					gutil.getOpposingEncodedNeighborhood(grid.grid[:, :, 1], hueIndex, layerColumn, maxN, buckets=2),
					maxN, buckets=2
				)
				print(descriptionList)

				moveOffset = testGetMoveOffset(descriptionList)
				print('Move: ' + str(moveOffset))
				nextGrid.grid[hueIndex][layerColumn][1] -= grid.grid[hueIndex][layerColumn][1]
				nextGrid.grid[hueIndex][layerColumn + moveOffset] += grid.grid[hueIndex][layerColumn][1]

	print('\nAfter ' + str(currentRound) + ' round:')
	nextGrid.display()
	grid = nextGrid
	currentRound += 1



print('\nFinished simulation')
