
# from utils import text_from_image

# text = text_from_image('screenshot.png');
# print(text)

# import pytesseract
# import numpy as np
# import cv2

# img = cv2.imread('opencv.png')

# #  img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
# #img = cv2.resize(img, None, fx=2, fy=2)

# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# kernel = np.ones((1,1), np.uint8)
# #  img = cv2.dilate(img, kernel, iterations=1)
# #  img = cv2.erode(img, kernel, iterations=1)

# #  img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# cv2.imwrite('thresh.png', img)

# for psm in range(6,13+1):
#     config = '--oem 3 --psm %d' % psm
#     txt = pytesseract.image_to_string(img, config = config, lang='eng')
#     print('psm ', psm, ':',txt)


# import cv2
# import pytesseract
# from picamera.array import PiRGBArray
# from picamera import PiCamera

# import time

# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 30

# rawCapture = PiRGBArray(camera, size=(640, 480))

# start = time.time()

# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

# 	rawCapture.truncate(0)
# 	if (time.time() - start > 5):

# 		image = frame.array
# 		# cv2.imshow("Frame", image)

# 		text = pytesseract.image_to_string(image)
# 		# cv2.imshow("Frame", image)
# 		cv2.destroyAllWindows()
# 		break

# print(text)


# import cv2 
# import pytesseract
# from picamera.array import PiRGBArray
# from picamera import PiCamera

# camera = PiCamera()
# camera.resolution = (640, 480)
# camera.framerate = 30

# rawCapture = PiRGBArray(camera, size=(640, 480))

# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
# 	image = frame.array
# 	cv2.imshow("Frame", image)
# 	key = cv2.waitKey(1) & 0xFF
	
# 	rawCapture.truncate(0)

# 	if key == ord("s"):
# 		text = pytesseract.image_to_string(image)
# 		print(text)
# 		cv2.imshow("Frame", image)
# 		cv2.waitKey(0)
# 		break

# cv2.destroyAllWindows()

import cv2
import numpy as np
from PIL import Image
import pytesseract



# def getSkewAngle(cvImage):
#     # Prep image, copy, convert to gray scale, blur, and threshold
#     newImage = cvImage.copy()
#     # gray = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(newImage, (9, 9), 0)
#     # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#     # Apply dilate to merge text into meaningful lines/paragraphs.
#     # Use larger kernel on X axis to merge characters into single line, cancelling out any spaces.
#     # But use smaller kernel on Y axis to separate between different blocks of text
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 5))
#     dilate = cv2.dilate(blur, kernel, iterations=5)

#     # Find all contours
#     contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key = cv2.contourArea, reverse = True)

#     # Find largest contour and surround in min area box
#     largestContour = contours[0]
#     minAreaRect = cv2.minAreaRect(largestContour)

#     # Determine the angle. Convert it to the value that was originally used to obtain skewed image
#     angle = minAreaRect[-1]
#     if angle < -45:
#         angle = 90 + angle
#     return -1.0 * angle

# def rotate_image(image, angle):
#   image_center = tuple(np.array(image.shape[1::-1]) / 2)
#   rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
#   result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
#   return result



# # Grayscale image
# img = Image.open('opencv.png').convert('L')
# ret, img = cv2.threshold(np.array(img), 125, 255, cv2.THRESH_BINARY)

# # Older versions of pytesseract need a pillow image
# # Convert back if needed
# # img = Image.fromarray(img.astype(np.uint8))

# # resize
# RESIZE_FACTOR = 1.4;
# new_width = int(img.shape[1] * RESIZE_FACTOR);
# new_height = int(img.shape[0] * RESIZE_FACTOR);
# dim = (new_width, new_height)
# img = cv2.resize(img, dim);

# # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # grayscaling
# # ret, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY) # thresholding

# # deskew img
# skew_angle = getSkewAngle(img);
# img = rotate_image(img, skew_angle);


# image = cv2.imread('captured.png');

# # resize image
# RESIZE_FACTOR = 2;
# width = int(image.shape[1] * RESIZE_FACTOR);
# height = int(image.shape[0] * RESIZE_FACTOR);
# dim = (width, height);
# resized = cv2.resize(image, dim);

# # gray_scale image
# gray_scale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY);

# # thresholded
# ret, thresholded = cv2.threshold(gray_scale, 127, 255, cv2.THRESH_BINARY);

# print(pytesseract.image_to_string(thresholded, lang='eng').strip())









# import pigpio
# from time import sleep

# pi = pigpio.pi()
# SERVO = 17

# MIN_PW = 1000
# MID_PW = 1500
# MAX_PW = 2000

# pi.set_servo_pulsewidth(SERVO, MIN_PW);
# sleep(3);

# pi.set_servo_pulsewidth(SERVO, MAX_PW);
# sleep(3);

# pi.set_servo_pulsewidth(SERVO, MID_PW);
# sleep(3);






from utils import date_from_timestamp, now

print(date_from_timestamp(now()))


