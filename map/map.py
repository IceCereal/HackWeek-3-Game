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
		self.keyPoint = (0, 0)

		self.grid = []

		if self.verbose:
			print ("\nStart: Making Grid...")
		self.__make_grid(image)

		self.__set_extra()

	def __make_grid(self, image : np.array):
		(height, width, depth) = image.shape

		self.width = int(width / self.pixelSize)
		self.height = int(height / self.pixelSize)

		if self.verbose:
			print ("Determined Values:")
			print ("Width:\t", self.width, "\nHeight:\t", self.height)

		if self.verbose:
			print ("\nScouting for new colors...")

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

		if self.verbose:
			print ("Completed getting colors!")

		if (255, 255, 255) not in self.reference_colors_index:
			if self.verbose:
				print ("\nBrute Adding (256, 256, 256)...")

			self.reference_colors_index.append((256, 256, 256))
			self.reference_colors[(256, 256, 256)] = (self.height * 4) + (self.width * 4) - 16
		else:
			print ("Manual Input Required! Exiting")
			exit()

		print (self.reference_colors)
		print ("\n", self.reference_colors_index)

		if self.verbose:
			print ("Getting most prevalent colors...")

		# Determine the wall's color
		sorted_colors = list(sorted(self.reference_colors.items(), key=operator.itemgetter(1), reverse=True))
		wall_color = sorted_colors[-1][0]

		if self.verbose:
			print ("Determined Wall Color:\t", wall_color)

		if self.verbose:
			print ("Begin Translation from array to grid...")

		# Make boundaries for the top part of the grid
		for line in range(2):
			tempLine = []
			for boundaryUnit in range(0, self.width + 4):
				color = (256, 256, 256)
				pixel = {
					'color' : self.reference_colors_index.index(color),
					'extras' : {
							'wall' : True,
							'boundary' : True
					}
				}
				tempLine.append(pixel)
			self.grid.append(tempLine)

		for line in range(0, height, self.pixelSize):
			tempLine = []

			# 2 Boundary units on the left side of the line
			for boundaryUnit in range(2):
				color = (256, 256, 256)
				pixel = {
					'color' : self.reference_colors_index.index(color),
					'extras' : {
							'wall' : True,
							'boundary' : True
					}
				}
				tempLine.append(pixel)

			for pixelUnit in range(0, width, self.pixelSize):
				color = str(image[line][pixelUnit])
				if color[1] == ' ':
					color = color.replace(' ', '', 1)
				color = color.replace("  ", " ", 10)
				color = color.replace(" ", ", ", 10)

				color = literal_eval(color)
				color = tuple(color)

				isWall = False
				if (color == wall_color):
					isWall = True

				pixel = {
					'color' : self.reference_colors_index.index(color),
					'extras' : {
							'wall' : isWall,
							'boundary' : False
					}
				}
				tempLine.append(pixel)

			# 2 Boundary units on the right side of the line
			for boundaryUnit in range(2):
				color = (256, 256, 256)
				pixel = {
					'color' : self.reference_colors_index.index(color),
					'extras' : {
							'wall' : True,
							'boundary' : True
					}
				}
				tempLine.append(pixel)

			self.grid.append(tempLine)

		# Make boundaries for the bottom part of the grid
		for line in range(2):
			tempLine = []
			for boundaryUnit in range(0, self.width + 4):
				color = (256, 256, 256)
				pixel = {
					'color' : self.reference_colors_index.index(color),
					'extras' : {
							'wall' : True,
							'boundary' : True
					}
				}
				tempLine.append(pixel)
			self.grid.append(tempLine)

		if self.verbose:
			print ("\nComplete: Making Grid!")
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
			print ("\nDetermining Values...")
	
		self.startPoint = (2 + randint(0, self.width - 1), 2 + 0)
		sleep( (randint(1, 1000)%5) / 5)
		self.endPoint = (2 + randint(0, self.width - 1), 2 + self.height-1)
		sleep( (randint(1, 1000)%5) / 6)

		# In case key is set on a wall
		def setKey():
			self.keyPoint = ( 2 + randint(0, self.width-1), 2 + randint(0, self.height-1) )

		for i in range(10):
			setKey()

			if self.grid[self.keyPoint[0]][self.keyPoint[1]]['extras']['wall'] == False:
				break

			if self.verbose:
				print ("Key Randomized to wall. Key Resetting (Attempt #", i+1, ")...")

		if i == 10:
			if self.verbose:
				print ("Key Randomized to wall more than 10 times.\nExiting...")
				exit()

		if self.verbose:
			print ("Starting At:\t", self.startPoint)
			print ("Ending At:\t", self.endPoint)
			print ("Key At:\t", self.keyPoint)