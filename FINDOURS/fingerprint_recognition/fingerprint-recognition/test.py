import cv2
from skimage.morphology import skeletonize, thin
import numpy
import matplotlib.pyplot as plt
import os
import sys
from enhance import image_enhance
import time

def get_descriptors(img):
    # applying image contrast
	clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	img = clahe.apply(img)

	img = image_enhance.image_enhance(img)
	img = numpy.array(img, dtype=numpy.uint8) # converting array-items datatype to int

	# Threshold
	ret, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
	# Normalize to 0 and 1 range
	img[img == 255] = 1

	#Thinning
	skeleton = skeletonize(img)
	skeleton = numpy.array(skeleton, dtype=numpy.uint8)

	# Harris corners
	harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)
	harris_normalized = cv2.normalize(harris_corners, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
	threshold_harris = 125

	# Extracting image keypoints
	keypoints = []
	for x in range(0, harris_normalized.shape[0]):
		for y in range(0, harris_normalized.shape[1]):
			if harris_normalized[x][y] > threshold_harris:
				keypoints.append(cv2.KeyPoint(y, x, 1))

	# Define descriptor
	orb = cv2.ORB_create()
	# Compute descriptors
	_, des = orb.compute(img, keypoints)
	return (keypoints, des);

res = cv2.imread("C:/Abhi/XAMPP/htdocs/FindOURS/fingerprint_recognition/fingerprint-recognition/database/101_8.tif", cv2.IMREAD_GRAYSCALE)
kp, des= get_descriptors(res);

print(des)