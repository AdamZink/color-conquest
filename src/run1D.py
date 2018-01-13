from grid_util import GridUtil as gutil
from neighborhood_util import NeighborhoodUtil as nutil
import numpy as np

gridColumns = 3
gridHueList = [0, 120]
maxN = 2

layers = np.zeros(shape=(len(gridHueList), gridColumns))
layers[1][2] = 1

print('\nInitial:')
print(layers)

for hueIndex in range(len(gridHueList)):
	for layerColumn in range(gridColumns):
		descriptionList = nutil.describeEncodedNeighborhood(
			gutil.getOpposingEncodedNeighborhood(layers, hueIndex, layerColumn, maxN, buckets=2),
			maxN, buckets=2
		)

		if (len(descriptionList) > 0):
			print('Hue index ' + str(hueIndex) + ', layer column index ' + str(layerColumn) + ':')
			print(descriptionList)

print('\nFinished simulation')
