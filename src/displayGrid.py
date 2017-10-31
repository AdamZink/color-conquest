from grid import Grid

gridRows = 2
gridColumns = 2
gridHueList = [60, 120]

grid = Grid(gridRows, gridColumns, gridHueList)

grid.display()

grid.setRandom(0.5, 3)

grid.display()
