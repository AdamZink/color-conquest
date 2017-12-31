from neighborhood_util import NeighborhoodUtil as nutil
import numpy as np

gridColumns = 3
gridHueList = [0, 120]
maxN = 2

layers = np.zeros(shape=(len(gridHueList), gridColumns))
layers[0][0] = 1
layers[1][1] = 1
layers[1][2] = 1

print('\nInitial:')
print(layers)

layer1 = layers[0]
layer2 = layers[1]

print('\nLayer 1 - check for units in layer 2')
for i in range(layer1.size):
	if (layer1[i] > 0):
		print('i = ' + str(i))
		print(nutil.describeEncodedNeighborhood(
			nutil.getEncodedNeighborhood(layer2, i, maxN),
			maxN
		))

print('\nLayer 2 - check for units in layer 1')
for j in range(layer2.size):
	if (layer2[j] > 0):
		print('j = ' + str(j))
		print(nutil.describeEncodedNeighborhood(
			nutil.getEncodedNeighborhood(layer1, j, maxN),
			maxN
		))

print('\nFinished simulation')
