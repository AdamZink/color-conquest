import numpy as np

class Grid:

	def __init__(self, rows, columns, colors):
		self.rows = rows
		self.columns = columns
		self.colors = colors
		# There are 3 attributes for each of the color cells:
		# 1) hue
		# 2) units
		# 3) collective experience (cannot be higher than 10 times the number of units?)
		self.grid = np.zeros(shape=(rows, columns, colors, 3))
	
	
	def getRowCount(self):
		return self.rows
		
	def getColumnCount(self):
		return self.columns
		
	def getColorCount(self):
		return self.colors
	
	
	def display(self):
		print(self.grid)
