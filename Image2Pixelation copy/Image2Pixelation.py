from PIL import Image
import numpy as np
import cv2

def Img2Pix(imagePath, K_Colors, pixelSize)
	imagePath = imagePath
	dest_Path = imagePath[0:imagePath.index('.')] + "_pixelated" + imagePath[imagePath.index('.'):]
	K_Colors = K_Colors
	pixelsize = pixelsize

	"""
		Segmentation
	"""
	img = cv2.imread(imagePath)
	Z = img.reshape((-1,3))

	Z = np.float32(Z)

	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	ret,label,center=cv2.kmeans(Z,K_Colors,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

	center = np.uint8(center)
	res = center[label.flatten()]
	res2 = res.reshape((img.shape))

	cv2.imwrite(dest_Path, res2)

	"""
		Pixelation
	"""
	image = Image.open(dest_Path)
	image = image.resize(
		(image.size[0] // pixelsize, image.size[1] // pixelsize),
		Image.NEAREST
	)
	image = image.resize(
		(image.size[0] * pixelsize, image.size[1] * pixelsize),
		Image.NEAREST
	)
	image.save(dest_Path)
	return np.array(image)