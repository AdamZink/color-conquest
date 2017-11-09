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
		f.write('<defs id="blend">\n')
		f.write('\t<filter id="blendFilter" style="color-interpolation-filters:sRGB">\n')
		f.write('\t\t<feBlend id="screenBlend" in2="BackgroundImage" mode="lighten" />\n')
		f.write('\t</filter>\n')
		f.write('</defs>\n')

		f.write('\n<g id="background">\n')
		f.write('\t<rect x="0" y="0" width="' + str(int(cellSize*g.columns)) + '" height="' + str(int(cellSize*g.rows)) + '" style="fill:rgb(0,0,0)" />\n')
		f.write('</g>\n\n')

		allUnits = 0
		for hueIndex in range(len(g.hueList)):
			f.write('\n<g id="hue' + str(g.hueList[hueIndex])+ '" style="filter:url(#blendFilter)">\n')

			for row in range(g.rows):
				for column in range(g.columns):

					lightness = 0.5
					saturation = 1.0

					opacityPower = 0.5  # make this higher to give brighter colored cells

					unitCount = g.grid[row, column, hueIndex, g.GRID_UNIT_INDEX]

					if(unitCount > 0):
						rgbTuple = hsv2rgb(getNormalizedHue(g.hueList[hueIndex]), saturation, lightness)
						opacity = 1.0 - (1.0 / ((g.grid[row, column, hueIndex, g.GRID_UNIT_INDEX] + 1)**opacityPower))

						f.write('\t<rect x="' + str(int(column*cellSize)) + '" y="' + str(int(row*cellSize)) + '" width="' + str(int(cellSize)) + '" height="' + str(int(cellSize)) + '" style="fill:' + rgbTupleToSvgString(rgbTuple) + ';opacity:' + str(opacity) + '" />\n')
						allUnits += unitCount

			f.write('</g>\n')

		f.write('</svg>\n')

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
