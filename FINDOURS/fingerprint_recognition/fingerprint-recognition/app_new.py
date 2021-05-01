import cv2
from skimage.morphology import skeletonize, thin
import numpy
import os
import pickle
import sys
import json
from enhance import image_enhance
import time

time1 = time.time() # Start time of program execution

# Changing current directory to project directory
os.chdir("C:/Abhi/XAMPP/htdocs/FindOURS/FINDOURS/fingerprint_recognition/fingerprint-recognition/")


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


def main(img1):
	des1 = bytes.fromhex(data[img1]["des"]) # Converting image description from hex to bytes
	des1 = pickle.loads(des1) # loading original image description

	# Matching between descriptors using bruteforce matching
	bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
	matches = sorted(bf.match(des1, des2), key= lambda match:match.distance)

	# Calculate score based on matches
	score = 0;
	for match in matches:
	    score += match.distance
	score_threshold = 33
	if score/len(matches) < score_threshold:
		# print(score/len(matches))
		return (True, data[img1])
	else:
		return (False, False)
	

def matcher():
	path_to_database = "C:/Users/SAI/Desktop/FindOURS/fingerprint_recognition/fingerprint-recognition/database/"
	img_list = [img for img in os.listdir(path_to_database) if os.path.isfile(os.path.join(path_to_database, img))]

	for img_path in img_list:
		hasMatched, matched_img = main(img_path)

		if hasMatched:
			# print(matched_img["name"])
			# print(hasMatched)
			print(img_path)
			# print(matched_img["age"])
			# return (matched_img["name"], matched_img["age"])
			break;

		if img_path == img_list[-1]:
			print("NMF") 


# Get input image descriptors
image_name = sys.argv[1]
img2 = cv2.imread("C:/Abhi/XAMPP/htdocs/FindOURS/FINDOURS/fingerprint_recognition/fingerprint-recognition/db2/" + image_name, cv2.IMREAD_GRAYSCALE)
kp2, des2 = get_descriptors(img2)


# Load image data from json
with open("C:/Users/SAI/Desktop/FindOURS/fingerprint_recognition/fingerprint-recognition/data.json", "r") as file:
	data = json.load(file)


if __name__ == "__main__":
    try:
        matcher()
    except:
        raise

time2 = time.time()
# print("Time to scan: ", time2-time1)