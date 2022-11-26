import urllib.request

import cv2
import pickle

import cvzone as cvzone
import numpy as np

import pyrebase

config = {
    'apiKey': "AIzaSyADtb8YcHBNJBb7ciA27K6PSUmNHn2ZMfc",
    'authDomain': "smart-parking-a60aa.firebaseapp.com",
    'databaseURL': "https://smart-parking-a60aa-default-rtdb.firebaseio.com/",
    'storageBucket': "smart-parking-a60aa.appspot.com"
}

firebase = pyrebase.initialize_app(config)

bd = firebase.database()

parking_spots_status = [False, False, False, False, False,
                        False, False, False, False, False]

bd.child().update({"parking_slots": parking_spots_status})

width, height = 90, 190

url = 'http://192.168.137.142/'

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)


def checkParkingSpace():
    for i, pos in enumerate(posList):
        x, y = pos
        # cv2.rectangle(img, pos, (x+width, y+height), (255, 0, 255), 2)
        imgCrop = imgMedian[y:y + height, x:x + width]
        #cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img, str(count), (x, y + height - 5), scale=1.5,
                           thickness=2, offset=0, colorR=(0, 0, 0))

        if count < 2000:
            color = (0, 255, 0)
            parking_spots_status[i] = False
        else:
            color = (0, 0, 255)
            parking_spots_status[i] = True

        cv2.rectangle(img, pos, (x + width, y + height), color, 1)
        bd.child().update({"parking_slots": parking_spots_status})


while True:

    img_url = urllib.request.urlopen(url)
    img_np = np.array(bytearray(img_url.read()), dtype=np.uint8)
    try:
        img = cv2.imdecode(img_np, -1)
    except:
        pass
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgThreshold = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 15, 6)
    imgMedian = cv2.medianBlur(imgThreshold, 5)

    checkParkingSpace()
    cv2.imshow('image', img)
    cv2.waitKey(1)
