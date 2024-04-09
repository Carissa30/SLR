#requirments
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
import time

# this func processes hand by cropping it from frame, then resizes it based on the dimensions given, and returns processed image
def process_hand(hand, img, offset, imgSize):
    x, y, width, height = hand['bbox']
    imgCrop = img[y - offset:y + height + offset, x - offset:x + width + offset]


    if imgCrop.shape[0] <= 0 or imgCrop.shape[1] <= 0:  # if image has valid dimensions
        return np.ones((imgSize, imgSize, 3), np.uint8) * 255  # returns a white img

    # the if-else block checks whether the hand is predominantly vertical or horizontal
    # and resizes it to fith within a square white canvas (in our case 300 x 300)  while maintaining the original hand's aspect ratoi
    # aspect ratio of hand's bounding box
    aspectRatio = height / width
    # height > width --> vertical hand orientation (eg. hand sign of the letter 'B')
    if aspectRatio > 1:
        # scaling factor for width
        scalingFactor = imgSize / height
        # width of the resized image is calculated to maintain aspect ratio
        widthCalculated = math.ceil(scalingFactor * width)
        # resize cropped hand to match widthCalculated and imgSize height
        imgResize = cv2.resize(imgCrop, (widthCalculated, imgSize))
        # imgResizeShape = imgResize.shape
        # gap needed to center the resized image in a white canvas
        widthGap = math.ceil((imgSize - widthCalculated) / 2)
        #create a white canvas of imgSize x imgSize dimensions
        whiteImg = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        #resized image is centered horizontally within the white canvas
        whiteImg[:, widthGap:widthCalculated + widthGap] = imgResize

    else:
        #scaling factor for height
        scalingFactor = imgSize / width
        #calculate height of resized image
        heightCalculated = math.ceil(scalingFactor * height)
        # resize cropped hand to match imgSize width and heightCalculated
        imgResize = cv2.resize(imgCrop, (imgSize, heightCalculated))
        # imgResizeShape = imgResize.shape
        #gap needed to center the resized image in a white canvas
        heightGap = math.ceil((imgSize - heightCalculated) / 2)
        # making a white canvas of imgSize x imgSize dimensions
        whiteImg = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        #resized image is centered vertically within the white canvas
        whiteImg[heightGap:heightCalculated + heightGap, :] = imgResize

    return whiteImg

# function reads a frame from camera (cap) and returns success status and captured frame (img)
def capture_frames(cap):
    success, img = cap.read()
    return success, img

# function for saving images
def save_image(image, folder, count):  # takes image and folder path as parameters
    cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', image) #  saves image with a timestamp in the specified folder
    print(count)

# main function
def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)  # detects only 1 hand at a time
    offset = 20
    imgSize = 300
    count = 0


    # continuously captures frames, detects hands, processes the detected hand, displays processed images
    while True:
        # captures frames
        success, img = capture_frames(cap)
        # processing hands
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            processed_img = process_hand(hand, img, offset, imgSize)
            cv2.imshow("Processed Image", processed_img)

        cv2.imshow("Original Image", img)
        key = cv2.waitKey(1)

        # Saving images
        if key == ord("s"):
            try:
                count = count + 1
                save_image(processed_img, "images/ambulance", count)
            except Exception as e:
                print(f"Error saving image: {e}")

        # when q is pressed loop breaks
        if key == ord("q"):
            break

    cap.release()  # camera is released
    cv2.destroyAllWindows()  # OpenCv windows are closed

if __name__ == "__main__":
    main()
