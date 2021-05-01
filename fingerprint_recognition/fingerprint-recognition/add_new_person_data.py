import json
import cv2, numpy, pickle
from skimage.morphology import skeletonize
from enhance import image_enhance 

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

    return des

path_to_database = "C:/Users/SAI/Desktop/FindOURS/fingerprint_recognition/fingerprint-recognition/database/"

name = input("Enter person's name: ")
age = int(input("Enter person's age: "))
address = input("Enter person's residential address: ")
fingerprint_name = input("Enter fingerprint name: ")

img = cv2.imread(path_to_database+fingerprint_name, cv2.IMREAD_GRAYSCALE) 
des = get_descriptors(img, fingerprint_name)

try:
    with open("C:/Users/SAI/Desktop/FindOURS/fingerprint_recognition/fingerprint-recognition/api/data.json", "r") as file:
        data = json.load(file)
        data[fingerprint_name]["name"] = name
        data[fingerprint_name]["age"] = age
        data[fingerprint_name]["address"] = address
        data[fingerprint_name]["des"] = pickle.dumps(des).hex()
        data = json.dumps(data)
        file.seek(0)
        file.write(data)
        file.truncate()
    
    print("Data added Successfully!")

except:
    raise