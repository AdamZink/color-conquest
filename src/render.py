import os, subprocess
import colorsys

def hsv2rgb(h,s,v):
	return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

def rgbTupleToSvgString(rgbTuple):
	return 'rgb(' + str(rgbTuple[0]) + ',' + str(rgbTuple[1]) + ',' + str(rgbTuple[2]) + ')'

def getNormalizedHue(hueFromGrid):
	return hueFromGrid / 360.0

def executeCommand(commandTokens):
	with open(os.devnull, 'wb') as devnull:
		p = subprocess.Popen(commandTokens, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	result = p.communicate()
	return result

def convertSvgToPng(svgPath, pngPath):
	#print(svgPath)
	#print(pngPath)
	result = executeCommand([
		'inkscape',
		svgPath,
		'--export-png=' + str(pngPath)
	])
	#print(result)

def renderGrid(g, imgName, cellSize):
	svgPath = os.path.join('..', 'img', 'svg', str(imgName) + '.svg')
	print(svgPath)
	with open(svgPath, 'w') as f:
		f.write('<?xml version="1.0"?>\n<!DOCTYPE svg>\n')
		f.write('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" width="' + str(int(g.columns*cellSize)) + '" height="' + str(int(g.rows*cellSize)) + '">\n')
		f.write('<g>\n')

		#f.write('\t<rect x="0" y="0" width="100" height="100" />\n\n')

		allUnits = 0
		for row in range(g.rows):
			for column in range(g.columns):

				lightness = 0.0
				saturation = 0.0

				lightnessPower = 0.8  # make this higher to give brighter colored cells

				unitSum = 0
				compositeHue = 0

				for hueIndex in range(len(g.hueList)):
					if(g.grid[row, column, hueIndex, g.GRID_UNIT_INDEX] > 0):
						unitSum += g.grid[row, column, hueIndex, g.GRID_UNIT_INDEX]
						# TODO derive the composite hue
						# reduce saturation if hue is mixed between 2 or more colors
						# short term - pick a color and reduce saturation
						if(compositeHue == 0):
							saturation = 1
							compositeHue = g.hueList[hueIndex]
							#print(g.hueList)
						elif(saturation > 0):
							saturation -= 0.25

				lightness = 1.0 - (1.0 / ((unitSum + 1)**lightnessPower))
				#print((getNormalizedHue(compositeHue), saturation, lightness))
				rgbTuple = hsv2rgb(getNormalizedHue(compositeHue), saturation, lightness)

				f.write('\t<rect x="' + str(int(column*cellSize)) + '" y="' + str(int(row*cellSize)) + '" width="' + str(int(cellSize)) + '" height="' + str(int(cellSize)) + '" style="fill:' + rgbTupleToSvgString(rgbTuple) + '" />\n')

				allUnits += unitSum

		f.write('</g>\n</svg>\n')

	# rasterize to PNG
	pngPath = os.path.join('..', 'img', 'png', str(imgName) + '.png')
	print(pngPath)
	convertSvgToPng(svgPath, pngPath)

	print('Total Units: ' + str(allUnits))

def exportVideo(g, videoName, framesPerSecond):
	videoPath = os.path.join('..', 'video', str(videoName) + '.mp4')
	command = 'ffmpeg -framerate ' + str(int(framesPerSecond)) + ' -i ../img/png/' + str(videoName) + '%d.png -pix_fmt yuv420p ' + videoPath + ' -y'

	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	result = process.communicate()

	for line in result:
		print (line)

	print ('Finished generating video')
