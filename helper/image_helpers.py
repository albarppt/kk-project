from skimage.filters import threshold_local
import numpy as np
import cv2 as cv
import imutils
import itertools
import skimage
import skimage.io
import base64
from io import BytesIO
from PIL import Image
from glob import glob


""" Load the image as numpy array (unchanged)

Returns:
	array -- Image pixels in numpy array (b, g, r)
"""


def load_original(filename):
	image = cv.imread(filename)

	if image is None:
		print('Error opening image: ' + filename)
		return []

	return image


""" Load the image as numpy array (grayscale)

Returns:
	array -- Grayscale image pixels in numpy array
"""


def load_grayscale(filename):
	image = cv.imread(filename)

	if image is None:
		print('Error opening image: ' + filename)
		return -1

	image = grayscale_conversion(image)

	return image


""" Convert image into grayscale
	Takes an RGB image and converts it into a grayscale image

Returns:
	array -- Grayscale image pixels in numpy array
"""


def grayscale_conversion(image):
	if len(image.shape) != 2:
		image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)  # grayscale conversion
	else:
		image = image

	return image


""" Blur convolutional operation (Gaussian)
	Default kernel size: 5x5
	Converts the image into grayscale if it hasn't been done

Returns:
	array -- Grayscale image pixels in numpy array
"""


def smoothen_image(image, size=5):
	gray = grayscale_conversion(image)

	gray = cv.GaussianBlur(gray, (size, size), 0)

	return gray


""" Remove all pixels in the top, left, right, and bottom with a certain size (padding)
	Converts the image into grayscale if it hasn't been done

Returns:
	array -- Grayscale image pixels in numpy array
"""


def remove_border(image, padding):
	gray = grayscale_conversion(image)

	h, w = gray.shape[:2]

	gray[0:padding, :] = 255
	gray[:, 0:padding] = 255
	gray[:, w-padding:w] = 255
	gray[h-padding:h, :] = 255

	return gray


""" Thresholding using Otsu's method
	Converts the image into grayscale if it hasn't been done

Returns:
	array -- Grayscale image pixels in numpy array
"""


def otsu_thresholding(image):
	gray = grayscale_conversion(image)
	return cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]


""" Bilateral filtering
	Smoothing image while preserving edges
	Converts the image into grayscale if it hasn't been done

Returns:
	array -- Grayscale image pixels in numpy array
"""


def bilateral_filter(image):
	image = cv.bilateralFilter(image, 10, 90, 90)

	return image


""" Applying gamma correction using power law transform
	From: https://www.pyimagesearch.com/2015/10/05/opencv-gamma-correction/

Returns:
	array -- Grayscale image pixels in numpy array
"""


def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
					  for i in np.arange(0, 256)]).astype("uint8")

	# apply gamma correction using the lookup table
	return cv.LUT(image, table)


""" Writes an image

Returns:
	None
"""


def write_image(filename, image):
	cv.imwrite(filename, image)


""" Normalizes an image, makes sure that the blackest parts of the image are more defined

Returns:
	array -- Image pixels in numpy array (b, g, r)
"""


def normalize_image(image):
	image = grayscale_conversion(image)

	if image is None or image.shape[0] <= 0 or image.shape[1] <= 0:
		return []

	image_copy = image.copy()

	mask = cv.dilate(image, np.ones((9, 9), np.uint8))

	mask = cv.medianBlur(mask, 21)

	diff = 255 - cv.absdiff(image_copy, mask)

	normalized = diff.copy()
	cv.normalize(diff, normalized, alpha=0, beta=255,
				 norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)

	normalized = cv.threshold(normalized, 230, 0, cv.THRESH_TRUNC)[1]
	cv.normalize(normalized, normalized, alpha=0, beta=255,
				 norm_type=cv.NORM_MINMAX, dtype=cv.CV_8UC1)

	return normalized


# From: https://stackoverflow.com/a/50444142
""" Encodes image to base64 string

Returns:
	string -- the base64 encoding result
"""


def encode(image):
	if len(image.shape) > 2:
		image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

	with BytesIO() as output_bytes:
		PIL_image = Image.fromarray(skimage.img_as_ubyte(image))
		# Note JPG is not a vaild type here
		PIL_image.save(output_bytes, 'PNG')
		bytes_data = output_bytes.getvalue()

	base64_str = str(base64.b64encode(bytes_data), 'utf-8')
	return base64_str


""" Decodes base64 string to numpy array

Returns:
	array -- the image
"""


def decode(base64_string):
	if isinstance(base64_string, bytes):
		base64_string = base64_string.decode("utf-8")

	imgdata = base64.b64decode(base64_string)
	img = skimage.io.imread(imgdata, plugin='imageio')

	img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

	return img

""" Increase the contrast of an image

Returns:
	array -- the image
"""

# From: https://stackoverflow.com/a/41075028
def increase_contrast(image):
	lab = cv.cvtColor(image, cv.COLOR_BGR2LAB)

	l, a, b = cv.split(lab)

	clahe = cv.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

	cl = clahe.apply(l)

	limg = cv.merge((cl, a, b))

	final = cv.cvtColor(limg, cv.COLOR_LAB2BGR)

	return final



#-------------------------------------------------------------------------------------------------#
"Added By: Albar PPT"

def image_ratio(img1, img2):
	return img1.shape[0] / float(img2.shape[0])

def show_image(name, image):
	cv.imshow(name, image)
	cv.waitKey(0)
	cv.destroyAllWindows()

def image_size(image):
	img_size = image.size // 1600
	print(img_size)


def load_all_images(img_dir=""):
	data = [cv.imread(file) for file in glob(img_dir)]
	return data
