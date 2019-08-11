import numpy as np
from collections import OrderedDict
import operator

class map:
	def __init__(self, image : np.array, pixelSize : int, verbose : bool = None,):
		if verbose == None:
			verbose = False
		self.verbose = verbose

		self.pixelSize = pixelSize
		self.height = 0
		self.width = 0
		self.reference_colors = {}
		self.reference_colors_index = []
		self.startPoint = (0, 0)
		self.endPoint = (0, 0)

		self.grid = []

		if self.verbose:
			print ("\nStart: Making Grid...")
		self.__make_grid(image, pixelSize)

		self.__set_extra()

	def __make_grid(self, image : np.array, pixelSize : int):
		(width, height, depth) = image.shape

		self.width = int(width / pixelSize)
		self.height = int(height / pixelSize)

		self.grid.append([{'color': -1, 'extra' : {'wall' : True}} for i in range(self.height+2)])
		for line in range(0, width, pixelSize):
			compressed_line = [{'color': -1, 'extra' : {'wall' : True}}]
			for pixelUnit in range(0, height, pixelSize):
				try:
					color = str(image[line][pixelUnit])
					if color[1] == ' ':
						color = color.replace(' ', '', 1)
					color = color.replace("  ", " ", 10)
					color = color.replace(" ", ", ", 10)
					
					if color not in self.reference_colors_index:
						if self.verbose:
							print ("Found New Color:\t", color)

						self.reference_colors_index.append(color)
						self.reference_colors[tuple(image[line][pixelUnit])] = 0

					pixel = {
						'color' : self.reference_colors_index.index(color),
						'extra' : {}
					}
					self.reference_colors[tuple(image[line][pixelUnit])] += 1

					compressed_line.append(pixel)
				except IndexError:
					pass
			compressed_line.append({'color': -1, 'extra' : {'wall' : True}})
			self.grid.append(compressed_line)
		self.grid.append([{'color': -1, 'extra' : {'wall' : True}} for i in range(self.height+2)])

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

	def __set_extra(self):
		if self.verbose:
			print ("\nStart: set_extra")

		if self.verbose:
			print ("Getting most prevalent colors...")
		
		sorted_colors = list(sorted(self.reference_colors.items(), key=operator.itemgetter(1), reverse=True))
		
		wall_color = sorted_colors[-1][0]
		wall_color_index = self.reference_colors_index.index(str(list(wall_color)))

		for line in self.grid:
			for pixel in line:
				if pixel['color'] == wall_color_index:
					pixel['extra']['wall'] = True
	
		self.startPoint = (1, 1)
		self.endPoint = (self.height, self.width)