from grid import Grid

gridRows = 2
gridColumns = 2
gridHueList = [60]

startingCellsWithUnits = 1
startingUnitCountPerCell = 10

grid = Grid(gridRows, gridColumns, gridHueList)
grid.setRandom(startingCellsWithUnits / (1.0* gridRows * gridColumns), startingUnitCountPerCell)

print('\nInitial:')
grid.display()

round = 1

while (round <= 10):
	grid.simulateRound()

	if (round == 1):
		print('\nAfter 1 round:')
	else:
		print('\nAfter ' + str(round) + ' rounds:')
	grid.display()
	
	round += 1
