import numpy as np
from collections import OrderedDict
import operator
from random import randint
from time import sleep
from ast import literal_eval

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
		self.key = (0, 0)

		self.grid = []

		if self.verbose:
			print ("\nStart: Making Grid...")
		self.__make_grid(image)

		self.__set_extra()

	def __make_grid(self, image : np.array):
		(height, width, depth) = image.shape

		self.width = int(width / self.pixelSize)
		self.height = int(height / self.pixelSize)

		print (self.width, self.height)

		for line in range(0, height, self.pixelSize):
			for pixelUnit in range(0, width, self.pixelSize):
				try:
					color = str(image[line][pixelUnit])
					if color[1] == ' ':
						color = color.replace(' ', '', 1)
					color = color.replace("  ", " ", 10)
					color = color.replace(" ", ", ", 10)

					color = literal_eval(color)
					color = tuple(color)

					if color not in self.reference_colors_index:
						if self.verbose:
							print ("Found New Color:\t", color)

						self.reference_colors_index.append(color)
						self.reference_colors[tuple(image[line][pixelUnit])] = 0

					self.reference_colors[tuple(image[line][pixelUnit])] += 1
				except IndexError:
					pass

		if (255, 255, 255) not in self.reference_colors_index:
			if self.verbose:
				print ("Adding (256, 256, 256)")

			self.reference_colors_index.append((256, 256, 256))
			self.reference_colors[(256, 256, 256)] = 
		else:
			print ("Manual Input Required! Exiting")
			exit()

		print (self.reference_colors)
		print ("\n", self.reference_colors_index)

		exit()

		for line in range(0, height, self.pixelSize):
			for pixelUnit in range(0, width, self.pixelSize):
				color = str(image[line][pixelUnit]))
				if color[1] == ' ':
						color = color.replace(' ', '', 1)
					color = color.replace("  ", " ", 10)
					color = color.replace(" ", ", ", 10)

					color = literal_eval(color)
					color = tuple(color)

		"""self.grid.append([{'color': -1, 'extra' : {'wall' : True}} for i in range(self.height+4)])
		for line in range(0, width, pixelSize):
			compressed_line = [{'color': -1, 'extra' : {'wall' : True}}, {'color': -1, 'extra' : {'wall' : True}}]
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
			compressed_line.append({'color': -1, 'extra' : {'wall' : True}})

			self.grid.append(compressed_line)
		self.grid.append([{'color': -1, 'extra' : {'wall' : True}} for i in range(self.height+4)])"""

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
	
		self.startPoint = (1, randint(1, self.height))
		sleep( (randint(1, 1000)%5) / 5)
		self.endPoint = (randint(1, self.height), self.width)