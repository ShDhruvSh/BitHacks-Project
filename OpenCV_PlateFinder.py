from imutils.perspective import four_point_transform
from imutils import contours
import imutils
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import detect_lp
from os.path import splitext, basename
from keras.models import model_from_json
import glob

%matplotlib inline


def load_model(path):
    try:
        path = splitext(path)[0]
        with open('%s.json' % path, 'r') as json_file:
            model_json = json_file.read()
        model = model_from_json(model_json, custom_objects={})
        model.load_weights('%s.h5' % path)
        return model
    except Exception as e:
        print(e)

wpod_net_path = "wpod-net.json"
wpod_net = load_model(wpod_net_path)

#change channels to normal, resizes images for displya if true
def preprocess_image(image_path,resize=True):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img / 255
    if resize:
        img = cv2.resize(img, (224,224))
    return img

#crop the image to the plate
def get_plate(image_path):
    Dmax = 608
    Dmin = 288
    vehicle = preprocess_image(image_path)
    ratio = float(max(vehicle.shape[:2])) / min(vehicle.shape[:2])
    side = int(ratio * Dmin)
    bound_dim = min(side, Dmax)
    _ , LpImg, _, cor = detect_lp(wpod_net, vehicle, bound_dim, lp_threshold=0.5)
    count = 0
    for img in LpImg:
        plt.imsave("scans/cropped" + str(count) + ".jpg", img)
        count += 1
    return LpImg

img = get_plate("PhotosToClean/download-4.jpg")[0]

def get_digits(image_path, lp_num):
    cropped = cv2.imread(image_path, cv2.CV_8UC1)
    image = imutils.resize(cropped, height=500)
    # operations to cleanup the thresholded image
    thresh = cv2.threshold(image, 0, 255,
    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    # find contours in the thresholded image, then initialize the
    # digit contours lists
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    digitCnts = []
    # loop over the digit area candidates
    count = 0
    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)
        # if the contour is sufficiently large, it must be a digit
        if (w <= 400)and (h >= 100):
            digitCnts.append(c)
            digit = image[y:y+h, x:x+w]
            plt.imsave("scans/digit"+ str(lp_num) + "-" + str(count)+".jpg", digit)
            count += 1
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0), 2)

# scan each plate in the image and get the digits
def scan_plate(image_path):
    lpImg = get_plate(image_path)
    count = 0
    for image in lpImg:
        path = "croppedImgs/cropped" + str(count) + ".jpg"
        get_digits(path, count)
        count += 1

scan_plate("PhotosToClean/download-4.jpg")
