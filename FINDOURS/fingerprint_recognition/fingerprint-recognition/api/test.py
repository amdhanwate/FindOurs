import json
import numpy as np
import pickle
with open("C:/Users/SAI/Desktop/FindOURS/fingerprint_recognition/fingerprint-recognition/data.json") as file:
    data = json.load(file)
    a= bytes.fromhex(data["101_1.tif"]["des"])
    print(pickle.loads(a))

    