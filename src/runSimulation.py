from grid import Grid
from render import renderGrid, exportVideo

gridRows = 36
gridColumns = 64
cellSize = 10
gridHueList = [0, 120, 240]

startingCellsWithUnits = 100*len(gridHueList)
startingUnitCountPerCell = 100

numberOfRounds = 16

grid = Grid(gridRows, gridColumns, gridHueList)
grid.setRandom(startingCellsWithUnits / (1.0 * gridRows * gridColumns), startingUnitCountPerCell)

# print('\nInitial:')
# grid.display()

renderGrid(grid, 'test0', cellSize)

round = 1

while (round <= numberOfRounds):
	grid.simulateRound()

	#print('\nAfter ' + str(round) + ' rounds:')
	#grid.display()

	renderGrid(grid, 'test' + str(round), cellSize)
	round += 1

exportVideo(grid, 'test', 4)

print('Finished simulating ' + str(round-1) + ' rounds')
