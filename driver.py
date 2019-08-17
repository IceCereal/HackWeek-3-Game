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
parser.add_argument('-v', "--verbose", action="store_true", help = "run driver and submodules with verbosity.")
parser.add_argument('-dpxs', '--displayPixelSize', type = int, required = True, help = "size of each pixel to be shown: (dpxs * ps) will be actual pixel size shown.")
parser.add_argument('-npx', '--numberPixels', type = int, help = "number of pixels to show per grid. (npx * npx) will be the number of pixels shown.")

opt = parser.parse_args()

imageArray = Img2Pix(imagePath = opt.imagePath, K_Colors = opt.numColors, pixelSize = opt.pixelSize, verbose = opt.verbose)
map = map(image = imageArray, pixelSize = opt.pixelSize, verbose = opt.verbose)

pygame.init()
window = pygame.display.set_mode((opt.displayPixelSize*map.pixelSize*opt.numberPixels, opt.displayPixelSize*map.pixelSize*opt.numberPixels))
background_color = (255, 255, 255)
window.fill(background_color)

def disp(me_x, me_y):
	a = [[0 for j in range(opt.numberPixels)] for i in range(opt.numberPixels)]
	for y in range(0, opt.numberPixels):
		for x in range(0, opt.numberPixels):
			yC = me_y - int(opt.numberPixels/2) + y
			xC = me_x - int(opt.numberPixels/2) + x

			try:
				a[y][x] = tuple(literal_eval(map.reference_colors_index[map.grid[xC][yC]['color']]))
			except IndexError:
				a[y][x] = (0, 0, 0)

			if (yC == map.startPoint[1]) and (xC == map.startPoint[0]):
				a[y][x] = (255, 255, 0)
			if (xC == map.endPoint[1]) and (yC == map.endPoint[0]):
				a[y][x] = (255, 255, 0)
	a[int(opt.numberPixels/2)][int(opt.numberPixels/2)] = (255, 0, 0)

	for y in range(0, opt.numberPixels):
		for x in range(0, opt.numberPixels):
			rect = pygame.Rect(y*map.pixelSize*opt.numberPixels, x*map.pixelSize*opt.numberPixels, map.pixelSize*opt.numberPixels, map.pixelSize*opt.numberPixels)
			pygame.draw.rect(window, a[y][x], rect)

	return


def loop():
	clock = pygame.time.Clock()
	me_x = map.startPoint[0]
	me_y = map.startPoint[1]

	while True:
		for event in pygame.event.get():
			queue_x = 0
			queue_y = 0
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_q:
					exit()
				if event.key == pygame.K_LEFT:
					queue_y = -1
				if event.key == pygame.K_RIGHT:
					queue_y = 1
				if event.key == pygame.K_UP:
					queue_x = -1
				if event.key == pygame.K_DOWN:
					queue_x = 1

		disp(me_x, me_y)

		if map.grid[me_x + queue_x][me_y + queue_y]['color'] != -1:
			try:
				if map.grid[me_x + queue_x][me_y + queue_y]['extra']['wall'] == True:
					pass
			except:
				me_x += queue_x
				me_y += queue_y

		pygame.display.update()
		clock.tick(25)

		if (me_x == map.endPoint[1]) and (me_y == map.endPoint[0]):
			print ("DONE")
			break

if __name__ == "__main__":
	loop()