import tensorflow as tf
import keras
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
import random
import pickle

img_width, img_height = 150, 150

train_data_dir = '/Users/jakewriter/PycharmProjects/BitHacks-project/PlateCharData'
catagories = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
              'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
              'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

'''
plt.imshow(img_array)
plt.show()
'''

trainingData = []
imgSize = 50
def createTrainingData():
    for catagory in catagories:
        path = os.path.join(train_data_dir, catagory)
        classNum = catagories.index(catagory)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img))
                resizedArray = cv2.resize(img_array, (imgSize, imgSize))
                trainingData.append([resizedArray, classNum])
            except Exception as e:
                pass

createTrainingData()

random.shuffle(trainingData)

X = []
Y = []

for features, label in trainingData:
    X.append(features)
    Y.append(label)

X = np.array(X).reshape(-1, imgSize, imgSize, 3)

pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

pickle_out = open("y.pickle", "wb")
pickle.dump(Y, pickle_out)
pickle_out.close()

pickle_in = open("X.pickle", "rb")
X = pickle.load(pickle_in)


validation_data_dir = '/yourdir/validation'
nb_train_samples = None #change this
nb_validation_samples = None #change this






