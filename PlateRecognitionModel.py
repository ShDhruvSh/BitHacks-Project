import tensorflow as tf
import keras
import struct
import random
import os
#import emnist
from emnist import list_datasets
from emnist import extract_test_samples
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.optimizers import SGD
import matplotlib.pyplot as plt
from keras.utils import to_categorical
import numpy as np
import cv2
import random
import pickle
from PIL import Image


'''
def createBetterTrainingData():# This is now worthless to me ;(
    thickTrainingData = []

    images, labels = extract_test_samples('digits')
    imagesL, labelsL = extract_test_samples('letters')

    images = images / 255 - 0.5
    imagesL = imagesL / 255 - 0.5
    images = images.reshape(-1, 784)
    imagesL = imagesL.reshape(-1, 784)


    for i in range(int(images.size/784)):
        thickTrainingData.append([images[i], labels[i]])
    for i in range(int(imagesL.size/784)):
        thickTrainingData.append([imagesL[i], labelsL[i] + 9])

    random.shuffle(thickTrainingData)


    X = []
    Y = []

    for features, label in thickTrainingData:
        X.append(features)
        Y.append(label)

    X = np.array(X)
    
    pickle_out = open("img.pickle", "wb")
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open("lab.pickle", "wb")
    pickle.dump(Y, pickle_out)
    pickle_out.close()
    

#createBetterTrainingData()


def trainWithBetterData(): # This is now worthless to me ;(


    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    #pickleImg_in = open("img.pickle", "rb")  # pickleImg_in = train_images
    #pickleLab_in = open("lab.pickle", "rb")  # pickleLab_in = train_labels
    #train_images = pickle.load(pickleImg_in)
    #train_labels = pickle.load(pickleLab_in)

    model = Sequential()

    model.add(Dense(64, activation='relu', input_dim=784))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(36, activation='softmax'))

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )


    #model.fit(train_images, to_categorical(train_labels), epochs=30, batch_size=32, validation_split=0.1)

    pickleX_in = open("X.pickle", "rb")  # pickleX_in = test_images
    pickleY_in = open("Y.pickle", "rb")  # pickleY_in = test_labels
    X = pickle.load(pickleX_in)/255.0 - 0.5
    Y = pickle.load(pickleY_in)

    accuracy = model.evaluate(
        X,
        to_categorical(Y)
    )

    print(accuracy)

    predictions = model.predict(X[:5])

    print(np.argmax(predictions, axis=1))
    print(Y[:5])

    for i in range(5):
        firstImage = X[i]
        firstImage = np.array(firstImage, dtype='float')
        pixels = firstImage.reshape(28, 28)
        plt.imshow(pixels)
        plt.show()


# 10 == 10 35 = 35

#trainWithBetterData()
'''

img_width, img_height = 150, 150
train_data_dir = '/Users/jakewriter/PycharmProjects/BitHacks-project/PlateCharData'
catagories = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13',
              '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27',
              '28', '29', '30', '31', '32', '33', '34', '35']

trainingData = []
imgSize = 28

'''
plt.imshow(img_array)
plt.show()
'''

def createTrainingData():
    for catagory in catagories:
        path = os.path.join(train_data_dir, catagory)
        classNum = catagories.index(catagory)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
                resizedArray = cv2.resize(img_array, (imgSize, imgSize))
                thresh = 100
                BWImage = cv2.threshold(resizedArray, thresh, 255, cv2.THRESH_BINARY)[1]


                numBlack = 0
                numWhite = 0
                for pix in np.nditer(BWImage):
                    if pix == 255:
                        numWhite += 1
                    else:
                        numBlack += 1
                if numWhite < numBlack:
                    BWImage = cv2.bitwise_not(BWImage)
                


                trainingData.append([BWImage, classNum])
            except Exception as e:
                pass

    random.shuffle(trainingData)

    X = []
    Y = []

    for features, label in trainingData:
        X.append(features)
        Y.append(label)

    X = np.array(X).reshape(-1, 784)


    pickle_out = open("X.pickle", "wb")
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open("Y.pickle", "wb")
    pickle.dump(Y, pickle_out)
    pickle_out.close()

#createTrainingData()

def tryNewTraining():
    pickleX_in = open("X.pickle", "rb")  # pickleX_in = test_images
    pickleY_in = open("Y.pickle", "rb")  # pickleY_in = test_labels
    X = pickle.load(pickleX_in)
    Y = pickle.load(pickleY_in)

    X = X / 255.0 - 0.5

    model = Sequential()

    model.add(Dense(64, activation='relu', input_dim=784))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(36, activation='softmax'))

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model.fit(X, to_categorical(Y), epochs=20, batch_size=16, validation_split=0.1)

    model.save_weights('model.h5')

tryNewTraining()


'''
This is now worthless to me ;(

pickleX_in = open("X.pickle", "rb") #pickleX_in = test_images
pickleY_in = open("Y.pickle", "rb") #pickleY_in = test_labels
X = pickle.load(pickleX_in)
Y = pickle.load(pickleY_in)

X = X/255.0 - 0.5

model = Sequential()

model.add(Conv2D(16, (3, 3), input_shape=X.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(16, (3, 3)))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(16))
model.add(Activation("relu"))

model.add(Dense(1))
model.add(Activation('sigmoid'))

#opt = SGD(lr=0.01)
model.compile(loss="categorical_crossentropy", optimizer="adam",
              metrics=['accuracy'])

model.fit(X, to_categorical(Y), batch_size=15, epochs=10, validation_split=0.1)

'''







