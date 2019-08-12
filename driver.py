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
parser.add_argument('-v', "--verbose", action="store_true", help="run driver and submodules with verbosity.")

opt = parser.parse_args()

imageArray = Img2Pix(imagePath = opt.imagePath, K_Colors = opt.numColors, pixelSize = opt.pixelSize, verbose = opt.verbose)
map = map(image = imageArray, pixelSize = opt.pixelSize, verbose = opt.verbose)

pygame.init()
window = pygame.display.set_mode((7*map.pixelSize*5, 7*map.pixelSize*5))
background_color = (255, 255, 255)
window.fill(background_color)

def disp(me_x, me_y):
	a = [[0, 0, 0, 0, 0, 0, 0, 0] for i in range(8)]
	for y in range(0, 8):
		for x in range(0, 8):
			yC = me_y - 3 + y
			xC = me_x - 3 + x

			try:
				a[y][x] = tuple(literal_eval(map.reference_colors_index[map.grid[xC][yC]['color']]))
			except IndexError:
				a[y][x] = (0, 0, 0)

			if (yC == map.startPoint[1]) and (xC == map.startPoint[0]):
				a[y][x] = (255, 255, 0)
			if (xC == map.endPoint[1]) and (yC == map.endPoint[0]):
				a[y][x] = (255, 255, 0)
	a[3][3] = (255, 0, 0)

	for y in range(0, 8):
		for x in range(0, 8):
			rect = pygame.Rect(y*map.pixelSize*5, x*map.pixelSize*5, map.pixelSize*5, map.pixelSize*5)
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