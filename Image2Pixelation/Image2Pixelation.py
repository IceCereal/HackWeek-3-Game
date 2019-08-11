from PIL import Image
import numpy as np
import cv2
from os import path

def Img2Pix(imagePath : str, K_Colors : int, pixelSize : int, verbose : bool = None):
	if verbose:
		print ("\nStart: Img2Pix...")
		print ("Image at:\t", imagePath)
		print ("K_Colors:\t", K_Colors)
		print ("Pixel Size:\t", pixelSize)

	file_name, ext = path.splitext(imagePath)
	dest_Path = file_name + "_pixelated.png"

	img = Image.open(imagePath)
	size = 1000, 800
	img.thumbnail(size)
	img.save(dest_Path)

	if verbose:
		print ("\nStart: Segmentation...")
	"""
		Segmentation
	"""
	img = cv2.imread(dest_Path)
	Z = img.reshape((-1,3))

	Z = np.float32(Z)

	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	ret,label,center=cv2.kmeans(Z,K_Colors,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

	center = np.uint8(center)
	res = center[label.flatten()]
	res2 = res.reshape((img.shape))

	cv2.imwrite(dest_Path, res2)\

	if verbose:
		print ("Complete: Segmentation!")

	if verbose:
		print ("\nStart: Pixelation...")

	"""
		Pixelation
	"""
	image = Image.open(dest_Path)
	image = image.resize(
		(image.size[0] // pixelSize, image.size[1] // pixelSize),
		Image.NEAREST
	)
	image = image.resize(
		(image.size[0] * pixelSize, image.size[1] * pixelSize),
		Image.NEAREST
	)
	image.save(dest_Path)

	if verbose:
		print ("Complete: Pixelation!")

	if verbose:
		print ("\nReturning: Numpy Array of Img2Pix(", dest_Path, ")")
	return np.array(image)