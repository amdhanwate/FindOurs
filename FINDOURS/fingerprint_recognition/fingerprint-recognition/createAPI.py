from os import path
import cv2
from skimage.morphology import skeletonize, thin
import numpy
from enhance import image_enhance
import json
from os import listdir
from os.path import isfile, join
import pickle

def get_descriptors(img, img_name):
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
    # skeleton = removedot(skeleton)

	# Harris corners
    harris_corners = cv2.cornerHarris(img, 3, 3, 0.04)
    harris_normalized = cv2.normalize(harris_corners, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32FC1)
    threshold_harris = 125

	# Extract keypoints
    keypoints = []
    for x in range(0, harris_normalized.shape[0]):
        for y in range(0, harris_normalized.shape[1]):
            if harris_normalized[x][y] > threshold_harris:
                keypoints.append(cv2.KeyPoint(y, x, 1))
	# Define descriptor
    orb = cv2.ORB_create()
	# Compute descriptors
    _, des = orb.compute(img, keypoints)
    # print(type(pickle.dumps(des)))
    # print(keypoints, end="\n\n\n\n")
    # print(type(des))
    # print(des.shape)
    with open("C:/Users/SAI/Desktop/FindOURS/fingerprint_recognition/fingerprint-recognition/data.json", "r+") as file:
        data = json.load(file)
        # print(data)
        # data[img]["kp"] = numpy.array(keypoints)
        data[img_name]["des"] = pickle.dumps(des).hex()
        data = json.dumps(data)
        file.seek(0)
        file.write(data)
        file.truncate()


    print(f"SUCCESSFULLY WROTE DESCRIPTORS FOR {img_name}")
	# return (keypoints, des);


# image_name = input("Enter image name: ")
# img = cv2.imread("database/"+image_name, cv2.IMREAD_GRAYSCALE)
# img = cv2.imread("C:/Users/SAI/Desktop/FindOURS/fingerprint_recognition/fingerprint-recognition/database/101_1.tif", cv2.IMREAD_GRAYSCALE)
# print(img)

path_to_database = "C:/Users/SAI/Desktop/FindOURS/fingerprint_recognition/fingerprint-recognition/database/"
img_list = [img for img in listdir(path_to_database) if isfile(join(path_to_database, img))]

for img_name in img_list:
    img = cv2.imread(path_to_database+img_name, cv2.IMREAD_GRAYSCALE)
    get_descriptors(img, img_name)