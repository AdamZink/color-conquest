import numpy as np
import random

class Grid1D:

	GRID_HUE_INDEX = 0
	GRID_UNIT_INDEX = 1

	NO_MOVE_INDEX = 0
	MOVE_POSITIVE_INDEX = 1
	MOVE_NEGATIVE_INDEX = 2

	moveDecode = {
		NO_MOVE_INDEX: (0),
		MOVE_POSITIVE_INDEX: (-1),
		MOVE_NEGATIVE_INDEX: (1)
	}

	#neighborhoodSize = 1

	def __init__(self, hueList, columns):
		self.hueList = hueList
		self.columns = columns

		self.moveDictionary = {}
		for hue in self.hueList:
			self.moveDictionary[hue] = {}

		# There are 2 attributes for each of the color cells:
		# 1) hue
		# 2) units
		self.grid = np.zeros(shape=(len(hueList), columns, 2))

		for hueIndex in range(len(hueList)):
			self.grid[hueIndex, :, self.GRID_HUE_INDEX] = self.hueList[hueIndex]

	def getColumnCount(self):
		return self.columns

	'''
	# Only intended to be called once after init when unit counts are all 0
	def setRandom(self, densityPercentage, unitsPerCell):
		randomValues = np.random.rand(self.rows, self.columns)
		colIndices, rowIndices = np.meshgrid(np.arange(randomValues.shape[1]),np.arange(randomValues.shape[0]))
		randomTable = np.vstack((randomValues.ravel(), rowIndices.ravel(), colIndices.ravel())).T

		sortedRandomTable = randomTable[randomTable[:,0].argsort()]
		selectedRandomTable = sortedRandomTable[0:int(sortedRandomTable.shape[0]*densityPercentage*1.0)]
		#print(selectedRandomTable)

		selectedRowIndex = 0
		colorIndex = 0

		for prob, row, col in selectedRandomTable:
			self.grid[int(row), int(col), colorIndex, 1] = unitsPerCell

			selectedRowIndex += 1

			# Use round robin pattern to assign units for each color
			colorIndex += 1
			if(colorIndex == len(self.hueList)):
				colorIndex = 0
	'''

	def display(self):
		print(self.grid)

	'''
	def getEncodedCell(self, row, column, hueIndex):
		# Encode 2 bit type per adjacent cell:
		# 0 - blocked, i.e. edge of grid
		# 1 - open, i.e. no colors
		# 2 - this color only
		# 3 - this color and 1 or more other colors also present

		if(row < 0 or row >= self.rows or column < 0 or column >= self.columns):
			return format(0, '02b')

		else:
			thisColorUnits = self.grid[row, column, hueIndex, self.GRID_UNIT_INDEX]
			allColorUnits = np.sum(self.grid[row, column, :, self.GRID_UNIT_INDEX])

			if(int(thisColorUnits) > 0 and int(thisColorUnits) == int(allColorUnits)):
				return format(2, '02b')
			elif(int(thisColorUnits) < int(allColorUnits)):
				return format(3, '02b')
			else:
				return format(1, '02b')

	def getNeighborhoodOffsetIndices(self):
		return np.arange((self.neighborhoodSize*2)+1) - self.neighborhoodSize

	def getRowNeighborhoodIndices(self, centerRow):
		return np.arange((self.neighborhoodSize*2)+1) - self.neighborhoodSize + centerRow

	def getColumnNeighborhoodIndices(self, centerColumn):
		return np.arange((self.neighborhoodSize*2)+1) - self.neighborhoodSize + centerColumn

	def getEncodedNeighborhood(self, centerRow, centerColumn, hueIndex):
		encodedString = ''
		for rowIndex in self.getRowNeighborhoodIndices(centerRow):
			for columnIndex in self.getColumnNeighborhoodIndices(centerColumn):
				encodedString += self.getEncodedCell(rowIndex, columnIndex, hueIndex)
		return encodedString

	def getPossibleMoves(self, centerRow, centerColumn, encodedString):
		encodedValues = [encodedString[i:i+2] for i in range(0, len(encodedString), 2)]
		possibleMoveTupleList = []
		rowOffsetList = self.getNeighborhoodOffsetIndices()
		columnOffsetList = self.getNeighborhoodOffsetIndices()
		valueIndex = 0
		for rowOffset in rowOffsetList:
			for columnOffset in columnOffsetList:
				if((rowOffset == 0 or columnOffset == 0) and encodedValues[valueIndex] != '00'):
					# the move is valid (not diagonal move AND not moving past an edge)
					possibleMoveTupleList.append((rowOffset, columnOffset))
				valueIndex += 1
		if(len(possibleMoveTupleList) == 0):
			print('SOMETHING IS WRONG')
			valueIndex = 0
			print('DEBUG:\n' + str(centerRow) + ', ' + str(centerColumn))
			for rowOffset in rowOffsetList:
				for columnOffset in columnOffsetList:
					print(str(rowOffset) + ', ' + str(columnOffset) + ' -> ' + str(self.isLeftRightUpDown(centerRow, centerColumn, rowOffset, columnOffset) and encodedValues[valueIndex] != '00'))
					valueIndex += 1
			exit()
		return possibleMoveTupleList


	def getNeighborhoodProbabilities(self, centerRow, centerColumn, encodedString):
		possibleMoveTupleList = self.getPossibleMoves(centerRow, centerColumn, encodedString)
		probArray = list(np.random.dirichlet(np.ones(len(possibleMoveTupleList)), size=1).flat)

		moveTupleList = []
		probIndex = 0
		for possibleMoveRowOffset, possibleMoveColumnOffset in possibleMoveTupleList:
			moveTupleList.append((possibleMoveRowOffset, possibleMoveColumnOffset, probArray[probIndex]))
			probIndex += 1

		return moveTupleList


	def simulateRound(self):
		# Make a copy with the before unit counts
		gridUnits = np.copy(self.grid[:, :, :, self.GRID_UNIT_INDEX])

		hueIndex = 0
		for hue in self.hueList:

			for row in np.arange(self.rows):
				for column in np.arange(self.columns):

					unitCount = int(gridUnits[row, column, hueIndex])

					if(unitCount > 0):
						encodedNeighborhood = self.getEncodedNeighborhood(row, column, hueIndex)

						if(encodedNeighborhood not in self.moveDictionary[hue]):
							# Set random probabilities based on encoded neighborhood
							self.moveDictionary[hue][encodedNeighborhood] = self.getNeighborhoodProbabilities(row, column, encodedNeighborhood)

						moveChoices = self.moveDictionary[hue][encodedNeighborhood]

						# print('Debug - Center: (' + str(row) + ', ' + str(column) + ')')
						# print('Debug - Move choices: ' + str(moveChoices))

						moveIndexChoices = []
						if(len(moveChoices) > 0):
							moveIndexChoices = np.random.choice(len(moveChoices), unitCount, p=[x[2] for x in self.moveDictionary[hue][encodedNeighborhood]])
							moveIndices, moveCount = np.unique(moveIndexChoices, return_counts=True)

						# resolve the moves to row and column indexes, but exclude "moves" where the unit is actually staying in place with 0,0 offset
						moveOffsets = [((moveChoices[moveIndices[i]][0], moveChoices[moveIndices[i]][1]), moveCount[i]) for i in np.arange(len(moveIndices)) if moveChoices[moveIndices[i]][0] != 0 or moveChoices[moveIndices[i]][1] != 0]

						moveDestinations = [((row + rowOffset, column + columnOffset), count) for ((rowOffset, columnOffset), count) in moveOffsets]

						# print('Debug - Selected move offsets: ' + str(moveOffsets))
						# print('Debug - Selected move destinations: ' + str(moveDestinations))

						for ((moveRow, moveColumn), count) in moveDestinations:
							self.grid[row, column, hueIndex, self.GRID_UNIT_INDEX] -= count
							self.grid[moveRow, moveColumn, hueIndex, self.GRID_UNIT_INDEX] += count

			hueIndex += 1
	'''
