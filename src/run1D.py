from grid_util import GridUtil as gutil
from neighborhood_util import NeighborhoodUtil as nutil
from grid_1D import *
from render import renderGrid, exportVideo

import numpy as np

gridHueList = [0, 120]
gridColumns = 16
maxN = 4
cellSize = 40

grid = Grid1D(gridHueList, gridColumns)
grid.grid[0][1][1] = 40
grid.grid[1][14][1] = 40


def testGetMoveOffset(descriptionList):
	for description in descriptionList:
		if 'Section +' in description:
			return 1
		elif 'Section -' in description:
			return -1
	return 0

numRounds = 16
currentRound = 1

print('\nInitial:')
grid.display()

renderGrid(grid, 'test1D_0', cellSize)

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
				nextGrid.grid[hueIndex][layerColumn + moveOffset][1] += grid.grid[hueIndex][layerColumn][1]

	print('\nAfter ' + str(currentRound) + ' rounds:')
	nextGrid.display()
	grid = nextGrid

	renderGrid(grid, 'test1D_' + str(currentRound), cellSize)

	currentRound += 1


exportVideo(grid, 'test1D_', 4)

print('\nFinished simulation')
