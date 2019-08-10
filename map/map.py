import contextlib
with contextlib.redirect_stdout(None):
	import pygame

import numpy as np

class map:
	def __init__(self, image : np.array, pixelSize : int, verbose : bool = None,):
		if verbose == None:
			verbose = False
		self.verbose = verbose

		self.pixelSize = pixelSize
		self.height = 0
		self.width = 0
		self.reference_colors = []
		self.grid = []

		if self.verbose:
			print ("\nStart: Making Grid...")
		self.make_grid(image, pixelSize)

	def make_grid(self, image : np.array, pixelSize : int):
		(width, height, depth) = image.shape
		reference_colors = []

		self.width = int(width / pixelSize)
		self.height = int(height / pixelSize)

		for line in range(0, width, pixelSize):
			compressed_line = []
			for pixelUnit in range(0, height, pixelSize):
				try:
					if str(image[line][pixelUnit]) not in reference_colors:
						if self.verbose:
							print ("Found New Color:\t", str(image[line][pixelUnit]))

						reference_colors.append(str(image[line][pixelUnit]))
						self.reference_colors.append(tuple(image[line][pixelUnit]))

					pixel = {
						'color' : reference_colors.index(str(image[line][pixelUnit])),
						'extra' : {}
					}

					compressed_line.append(pixel)
				except IndexError:
						pass
			self.grid.append(compressed_line)

		if self.verbose:
			print ("Complete: Making Grid!")
			print ("\nGrid Stats:")
			print ("Width:\t", self.width)
			print ("Height:\t", self.height)
			print ("Number of Colors Identified:\t", len(self.reference_colors))
			print ("Colors Identified:\t", self.reference_colors)
			print ("\nMap:\n")
			for line in self.grid:
				for pixel in line:
					print (pixel['color'], end=' ')
				print ("\n", end='')