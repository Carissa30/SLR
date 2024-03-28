import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import math

# Function for hand processing
def hand_processor(hand, img, offset, imgSize, classifier):
    x, y, width, height = hand['bbox']
    imgCrop = img[y - offset:y + height + offset, x - offset:x + width + offset]
    imgCropShape = imgCrop.shape

    if imgCrop.shape[0] <= 0 or imgCrop.shape[1] <= 0:  # if image has valid dimensions
        return np.ones((imgSize, imgSize, 3), np.uint8) * 255  # returns a white img

    aspectRatio = height / width
    if aspectRatio > 1:
        k = imgSize / height
        widthCalculated = math.ceil(k * width)
        imgResize = cv2.resize(imgCrop, (widthCalculated, imgSize))
        imgResizeShape = imgResize.shape
        widthGap = math.ceil((imgSize - widthCalculated) / 2)
        whiteImg = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        whiteImg[:, widthGap:widthCalculated + widthGap] = imgResize
        prediction, index = classifier.getPrediction(whiteImg)
        print(prediction, index)

    else:
        k = imgSize / width
        heightCalculated = math.ceil(k * height)
        imgResize = cv2.resize(imgCrop, (imgSize, heightCalculated))
        imgResizeShape = imgResize.shape
        heightGap = math.ceil((imgSize - heightCalculated) / 2)
        whiteImg = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        whiteImg[heightGap:heightCalculated + heightGap, :] = imgResize
        prediction, index = classifier.getPrediction(whiteImg)

    return whiteImg

# captures frames
def capture_frames(cap):
    success, img = cap.read()
    return success, img


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)
    offset = 20
    imgSize = 300

    classifier = Classifier("model/keras_model.h5", "model/labels.txt")

    labels = ["help","ambulance"]

    while True:
        success, img = capture_frames(cap)

        # Processing hands
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            processed_img = hand_processor(hand, img, offset, imgSize, classifier)
            cv2.imshow("Processed Image", processed_img)

        cv2.imshow("Original Image", img)
        key = cv2.waitKey(1)


        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
