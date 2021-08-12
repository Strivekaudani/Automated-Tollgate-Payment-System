
import cv2
import pytesseract
import os
import numpy as np
from threading import Thread;
from time import sleep;

os.system('clear')

def text_from_image(image):

	# resize image
	RESIZE_FACTOR = 3;
	width = int(image.shape[1] * RESIZE_FACTOR);
	height = int(image.shape[0] * RESIZE_FACTOR);
	dim = (width, height);
	resized = cv2.resize(image, dim);
	
	gray_scale = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY); # gray_scale image
	ret, thresholded = cv2.threshold(gray_scale, 90, 255, cv2.THRESH_BINARY); # thresholded

	return pytesseract.image_to_string(thresholded, lang='eng').strip(); # return detected text


# textDetector = TextDetector();
# textDetector.start();


# cv2.namedWindow("preview")
# vc = cv2.VideoCapture("http://10.42.0.20:5000/video-feed");

# if vc.isOpened(): # try to get the first frame
#    rval, frame = vc.read()
# else:
#    rval = False


# while rval:

# 	cv2.imshow("preview", frame)
# 	rval, frame = vc.read()
# 	key = cv2.waitKey(20)

# 	if (textDetector.text != ""):
# 		break

# 	image = np.array(frame);

# cv2.destroyWindow("preview")



# image = cv2.imread('/home/xavier/Desktop/opencv.png');
# cv2.imwrite('/home/xavier/Desktop/captured.png', image);


class CameraStreamer(Thread):

	def __init__(self, textDetector):
		Thread.__init__(self);
		self.textDetector = textDetector
		self.exit = False;

	def run(self):

		vc = cv2.VideoCapture("http://10.42.0.20:5000/video-feed");

		while True:

			if (self.exit):
				return;

			rval, frame = vc.read()
			if (rval):
				self.textDetector.image = np.array(frame);
				print("FRAME CAPTURED")
			else:
				print("RVAL IS FALSE")


class TextDetector(Thread):

	def __init__(self):
		Thread.__init__(self);
		self.cameraStreamer = CameraStreamer(self);
		self.exit = False;
		self.image = None;

	def run(self):

		self.cameraStreamer.start();

		while (True):


			if (self.exit):
				return;

			sleep(0.1);

			if (self.image is None):
				print("IMAGE IS NONE")
				continue;

			image = self.image.copy();

			text = text_from_image(image);
			cv2.imwrite('capture.png', image);
			print("Image written to disk")


			if (text != ''):

				print("===============================================================")
				print("DETECTED TEXT: " + text);
				print("===============================================================")

	def stop(self):
		self.cameraStreamer.exit = True;
		self.exit = True;


import socket

def get_ip_as_seen_by(remote_ip):

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
		s.connect((remote_ip, 1));
		IP = s.getsockname()[0];
	except Exception as e:
		print(str(e))
		IP = '127.0.0.1';
	finally:
		s.close();
		return IP;


image = cv2.imread('video-streaming-4.png');
cv2.imwrite('video-streaming-4.jpg', image)