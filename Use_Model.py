import tensorflow as tf
from keras.models import load_model
from keras.models import Sequential
from keras.layers import Dense
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

class predictionMethods():
    def __init__(self):
        pass
    def returnPrediction(self, imgFile):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        model = Sequential()
        model.add(Dense(64, activation='relu', input_dim=784))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(36, activation='softmax'))
        model.load_weights('model.h5')

        imgSize = 28

        imgPath = '/Users/jakewriter/PycharmProjects/BitHacks-project/scans/' + imgFile

        img_array = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
        resizedArray = cv2.resize(img_array, (imgSize, imgSize))
        thresh = 120
        BWImage = cv2.threshold(resizedArray, thresh, 255, cv2.THRESH_BINARY)[1]

        '''
        numBlack = 0
        numWhite = 0
        for pix in np.nditer(BWImage):
            if pix == 255:
                numWhite += 1
            else:
                numBlack += 1
        if numWhite < numBlack:
            BWImage = cv2.bitwise_not(BWImage)
        '''

        #plt.imshow(BWImage)
        #plt.show()

        BWImage = np.array(BWImage).reshape(-1, 784)



        predictions = model.predict(BWImage)
        prediction = np.argmax(predictions, axis=1)

        if prediction > 9:
            prediction = str(chr(prediction + 55))
        else:
            prediction = str(prediction)[1]



        return prediction

    def returnDigits(self):
        dir = './scans/'
        path = os.path.join(dir)
        plateNum = ""
        i = 0
        for img in os.listdir(path):
            # print(returnPrediction("Scan" + str(i + 15) + ".png"))
            plateNum += predictionMethods.returnPrediction(self, "digit0-" + str(i) + ".jpg")
            i += 1

        return plateNum
