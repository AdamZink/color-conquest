from grid import Grid
from render import renderGrid, exportVideo

gridRows = 16
gridColumns = 16
cellSize = 20
gridHueList = [0, 120, 240]

startingCellsWithUnits = 2*len(gridHueList)
startingUnitCountPerCell = 1

numberOfRounds = 8

grid = Grid(gridRows, gridColumns, gridHueList)
grid.setRandom(startingCellsWithUnits / (1.0* gridRows * gridColumns), startingUnitCountPerCell)

#print('\nInitial:')
#grid.display()
renderGrid(grid, 'test0', cellSize)

round = 1

while (round <= numberOfRounds):
	grid.simulateRound()

	# print('\nAfter ' + str(round) + ' rounds:')
	# grid.display()

	renderGrid(grid, 'test' + str(round), cellSize)

	round += 1

exportVideo(grid, 'test', 4)

print('Finished simulating ' + str(round-1) + ' rounds')
