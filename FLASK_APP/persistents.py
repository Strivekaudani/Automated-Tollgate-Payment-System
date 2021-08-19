
import cv2

feed_url = 'http://localhost:5000/video-feed'

class PersistantVC:

	def __init__(self):
		self.vc = cv2.VideoCapture(feed_url);


	def get_frame(self):

		if (not self.vc.isOpened()):
			self.vc = cv2.VideoCapture(feed_url);

		vc = self.vc;

		trials = 0;

		while (True):

			ret, frame = vc.read();

			if (ret):
				return frame;
				break

			trials = trials + 1;
			if (trials > 10):
				return frame;



persistent_vc = PersistantVC();