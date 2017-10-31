import numpy as np

class Grid:

	GRID_HUE_INDEX = 0
	GRID_UNIT_INDEX = 1
	GRID_SKILL_INDEX = 2

	def __init__(self, rows, columns, hueList):
		self.rows = rows
		self.columns = columns
		self.hueList = hueList
		
		# There are 3 attributes for each of the color cells:
		# 1) hue
		# 2) units
		# 3) collective skill (cannot be higher than 10 times the number of units?)
		self.grid = np.zeros(shape=(rows, columns, len(hueList), 3))
		
		hueIndex = 0
		for hue in hueList:
			self.grid[:, :, hueIndex, self.GRID_HUE_INDEX] = hue
			hueIndex += 1
	
	
	def getRowCount(self):
		return self.rows
		
	def getColumnCount(self):
		return self.columns
		
	def getColorCount(self):
		return self.colors
	
	
	# Only intended to be called once after init when unit counts are all 0
	def setRandom(self, densityPercentage, unitsPerCell):
		randomValues = np.random.rand(self.rows, self.columns)
		colIndices, rowIndices = np.meshgrid(np.arange(randomValues.shape[1]),np.arange(randomValues.shape[0]))
		randomTable = np.vstack((randomValues.ravel(), rowIndices.ravel(), colIndices.ravel())).T
		
		sortedRandomTable = randomTable[randomTable[:,0].argsort()]
		selectedRandomTable = sortedRandomTable[0:int(sortedRandomTable.shape[0]*densityPercentage*1.0)]
		print(selectedRandomTable)
		
		selectedRowIndex = 0
		colorIndex = 0
		
		for prob, row, col in selectedRandomTable:
			self.grid[int(row), int(col), colorIndex, 1] = unitsPerCell
			
			selectedRowIndex += 1
			
			# Use round robin pattern to assign units for each color
			colorIndex += 1
			if(colorIndex == len(self.hueList)):
				colorIndex = 0
			
	
	def display(self):
		print(self.grid)
