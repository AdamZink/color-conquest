import numpy as np

class Grid:

	def __init__(self, rows, columns, colors):
		self.rows = rows
		self.columns = columns
		self.colors = colors
		self.grid = np.zeros(shape=(rows, columns, colors, 2))
	
	
	def getRowCount(self):
		return self.rows
		
	def getColumnCount(self):
		return self.columns
		
	def getColorCount(self):
		return self.colors
	
	
	def display(self):
		print(self.grid)
