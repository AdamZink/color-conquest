from grid_util import GridUtil as gutil
from neighborhood_util import NeighborhoodUtil as nutil
import numpy as np

gridColumns = 4
gridHueList = [0, 120]
maxN = 2

layers = np.zeros(shape=(len(gridHueList), gridColumns))
layers[0][0] = 1
layers[1][3] = 1


def testGetMoveOffset(descriptionList):
	for description in descriptionList:
		if 'Section +' in description:
			return 1
		elif 'Section -' in description:
			return -1
	return 0


print('\nInitial:')
print(layers)

layers2 = np.copy(layers)

for hueIndex in range(len(gridHueList)):
	for layerColumn in range(gridColumns):
		if layers[hueIndex][layerColumn] > 0:
			print('\nHue index ' + str(hueIndex) + ', layer column index ' + str(layerColumn) + ':')

			descriptionList = nutil.describeEncodedNeighborhood(
				gutil.getOpposingEncodedNeighborhood(layers, hueIndex, layerColumn, maxN, buckets=2),
				maxN, buckets=2
			)
			print(descriptionList)

			moveOffset = testGetMoveOffset(descriptionList)
			print('Move: ' + str(moveOffset))
			layers2[hueIndex][layerColumn] -= 1
			layers2[hueIndex][layerColumn + moveOffset] += 1

print('\nAfter first round:')
print(layers2)

print('\nFinished simulation')
