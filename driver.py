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
window = pygame.display.set_mode(((map.height+2)*map.pixelSize, (map.width+2)*map.pixelSize))
background_color = (255, 255, 255)
window.fill(background_color)
print (map.height, map.width, map.pixelSize)

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

		for y in range(0, map.height+2):
			for x in range(0, map.width+2):
				rect = pygame.Rect(y*map.pixelSize, x*map.pixelSize, map.pixelSize, map.pixelSize)
				if (map.grid[x][y]['color'] == -1):
					pygame.draw.rect(window, (0, 0, 0), rect)
				else:
					pygame.draw.rect(window, tuple(literal_eval(map.reference_colors_index[map.grid[x][y]['color']])), rect)

		rect = pygame.Rect(map.startPoint[1]*map.pixelSize, map.startPoint[0]*map.pixelSize, map.pixelSize, map.pixelSize)
		pygame.draw.rect(window, (40, 40, 100), rect)

		rect = pygame.Rect(map.endPoint[0]*map.pixelSize, map.endPoint[1]*map.pixelSize, map.pixelSize, map.pixelSize)
		pygame.draw.rect(window, (40, 40, 100), rect)

		if map.grid[me_x + queue_x][me_y + queue_y]['color'] != -1:
			try:
				if map.grid[me_x + queue_x][me_y + queue_y]['extra']['wall'] == True:
					pass
			except:
				me_x += queue_x
				me_y += queue_y

		rect = pygame.Rect(me_y*map.pixelSize, me_x*map.pixelSize, map.pixelSize, map.pixelSize)
		pygame.draw.rect(window, (255, 0, 0), rect)
		pygame.display.update()
		clock.tick(45)

if __name__ == "__main__":
	loop()