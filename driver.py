### SUPER IMPORTANT NOTE!
### In this game, accessing an (x, y) must be done liek so: grid[y][x]

from argparse import ArgumentParser

from Image2Pixelation.Image2Pixelation import Img2Pix
from map.map import map

from ast import literal_eval

import contextlib
with contextlib.redirect_stdout(None):
	import pygame

parser = ArgumentParser()
parser.add_argument('-i', "--imagePath", type = str, required = True, help = "path to the image.")
parser.add_argument('-nc', "--numColors", type = int, required = True, help = "number of colors to be made.")
parser.add_argument('-ps', "--pixelSize", type = int, required = True, help = "size of each pixel to be made.")
parser.add_argument('-dpxs', '--displayPixelSize', type = int, required = True, help = "size of each pixel to be shown: (dpxs * ps) will be actual pixel size shown.")
parser.add_argument('-npx', '--numberPixels', type = int, help = "number of pixels to show per grid. (npx * npx) will be the number of pixels shown. keep this as odd.")
parser.add_argument('-v', "--verbose", action="store_true", help = "run driver and submodules with verbosity.")

opt = parser.parse_args()

imageArray = Img2Pix(imagePath = opt.imagePath, K_Colors = opt.numColors, pixelSize = opt.pixelSize, verbose = opt.verbose)
map = map(image = imageArray, pixelSize = opt.pixelSize, verbose = opt.verbose)

pygame.init()
window = pygame.display.set_mode((
				map.pixelSize * (opt.numberPixels-2) * opt.displayPixelSize, \
				map.pixelSize * (opt.numberPixels-2) * opt.displayPixelSize
				))
background_color = (0, 0, 0)
window.fill(background_color)

def disp(me_x, me_y):
	a = [[0 for j in range(opt.numberPixels)] for i in range(opt.numberPixels)]
	for y in range(0, opt.numberPixels):
		for x in range(0, opt.numberPixels):
			xC = me_x - int(opt.numberPixels/2) + x
			yC = me_y - int(opt.numberPixels/2) + y

			try:
				a[x][y] = map.reference_colors[map.grid[yC][xC]['color']]
			except IndexError:
				a[x][y] = (0, 0, 0)

			if (xC == map.startPoint[0]) and (yC == map.startPoint[1]):
				a[x][y] = (255, 255, 0)
			if (xC == map.endPoint[0]) and (yC == map.endPoint[1]):
				a[x][y] = (255, 255, 0)
			if (xC == map.keyPoint[0] and yC == map.keyPoint[1]):
				a[x][y] = (0, 255, 0)

	a[int(opt.numberPixels/2)][int(opt.numberPixels/2)] = (255, 0, 144)

	for y in range(0, opt.numberPixels):
		for x in range(0, opt.numberPixels):
			rect = pygame.Rect(x*map.pixelSize*opt.numberPixels, y*map.pixelSize*opt.numberPixels, map.pixelSize*opt.displayPixelSize, map.pixelSize*opt.displayPixelSize)
			pygame.draw.rect(window, a[x][y], rect)

	# for y in range(0, opt.numberPixels):
	# 	for x in range(0, opt.numberPixels):
	# 		print (a[x][y], end=' ')
	# 	print ("\n", end=' ')
	# exit()

	return


def loop():
	clock = pygame.time.Clock()
	me_x = map.startPoint[0]
	me_y = map.startPoint[1]

	while True:
		queue_x = 0
		queue_y = 0
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					exit()
				if event.key == pygame.K_LEFT:
					queue_x = -1
				if event.key == pygame.K_RIGHT:
					queue_x = 1
				if event.key == pygame.K_UP:
					queue_y = -1
				if event.key == pygame.K_DOWN:
					queue_y = 1

		disp(me_x, me_y)

		extraState = map.grid[me_y + queue_y][me_x + queue_x]['extras']

		if (extraState['wall'] == True) or (extraState['boundary'] == True):
			pass
		else:
			me_x += queue_x
			me_y += queue_y

		# Pick Up Key
		if (me_x == map.keyPoint[0] and me_y == map.keyPoint[1]):
				map.keyPoint = (-10, -10)

		pygame.display.update()
		clock.tick(25)

		if (me_x == map.endPoint[0]) and (me_y == map.endPoint[1]):
			print ("DONE")
			break

if __name__ == "__main__":
	loop()