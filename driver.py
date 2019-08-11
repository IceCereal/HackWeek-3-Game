from argparse import ArgumentParser

from Image2Pixelation.Image2Pixelation import Img2Pix
from map.map import map

parser = ArgumentParser()
parser.add_argument('-i', "--imagePath", type = str, required = True, help = "path to the image.")
parser.add_argument('-nc', "--numColors", type = int, required = True, help = "number of colors to be made.")
parser.add_argument('-ps', "--pixelSize", type = int, required = True, help = "size of each pixel to be made.")
parser.add_argument('-v', "--verbose", action="store_true", help="run driver and submodules with verbosity.")

opt = parser.parse_args()

imageArray = Img2Pix(imagePath = opt.imagePath, K_Colors = opt.numColors, pixelSize = opt.pixelSize, verbose = opt.verbose)
map = map(image = imageArray, pixelSize = opt.pixelSize, verbose = opt.verbose)
import pygame
pygame.init()
window = pygame.display.set_mode(((map.height+2)*map.pixelSize, (map.width+2)*map.pixelSize))
background_color = (255, 255, 255)
window.fill(background_color)
print (map.height, map.width, map.pixelSize)
for y in range(0, map.height+2):
	for x in range(0, map.width+2):
		rect = pygame.Rect(y*map.pixelSize, x*map.pixelSize, map.pixelSize, map.pixelSize)
		if (map.grid[x][y]['color'] == -1):
			pygame.draw.rect(window, (0, 0, 0), rect)
		else:
			pygame.draw.rect(window, tuple(map.reference_colors_values[map.grid[x][y]['color']]), rect)

pygame.display.flip()

# a = input()