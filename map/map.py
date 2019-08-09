import pygame
from argparse import ArgumentParser

class map:
	def __init__(self, verbose : bool = None):
		if verbose == None:
			verbose = False
		self.verbose = verbose

	def make_grid(self, width : int, height : int):
		if self.verbose:
			print ("Making Grid of Dimensions:\t", width, "w\t", height, "h...")

		map_pixel = {
			'color' : 0,
			'extras' : {}
		}

		self.grid = [[map_pixel for i in range(width)] for j in range(height)]

		if self.verbose:
			print ("Complete Making Grid!")


if __name__ == "__main__":
	parser = ArgumentParser()

	parser.add_argument('-wd', "--width", required=True, type=int, help="Width of the image")
	parser.add_argument('-ht', "--height", required=True, type=int, help="Height of the image")
	parser.add_argument('-v', "--verbose", required=False, action='store_true', help="Verbosity")

	opt = parser.parse_args()

	map = map(opt.verbose)
	map.make_grid(opt.width, opt.height)