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
	
	
	def display(self):
		print(self.grid)
