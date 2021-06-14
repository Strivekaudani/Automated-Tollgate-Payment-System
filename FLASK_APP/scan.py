
import cv2
import pytesseract
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera

from boom_gate import open_and_close
from utils import text_from_image

BOOM_GATE_FEE = 1

def scan_plates(request, response):


	# authentication;
	user = request.user;

	if (user == None):
	    return response.redirect_302('/notice?message=You need to login to access this page.');

	is_not_admin = not user["is_admin"];

	if (is_not_admin):
	    return response.redirect_302('/notice?message=You are not authorized to access this page.');
	
	try:

		# capture frame
		vc = cv2.VideoCapture('http://localhost:5000/video-feed');

		while (True):
			ret, frame = vc.read();

			if (ret):
				image = np.array(frame)
				break

		text = text_from_image(image)

		if (len(text) == 0):
			response.set_json_body('NO CAR DETECTED')
			response.status = 404
			return response.render();

		print('DETECTED TEXT:', text)

	   # querying the database
		db = request.db;
		query = { "cars.number_plate": text }
		projection = { "funds": 1, "email": 1 }

		user = db.users.find_one(query, projection);

		if (user == None):
			response.set_json_body('Car not recognized');
			response.status = 404;
			return response.render();

		# checking funds
		funds = user["funds"];

		fee = BOOM_GATE_FEE

		if (funds < BOOM_GATE_FEE):
			response.set_json_body('The driver\'s account has insufficient funds. We have added a debit on their account, and added a penalty of 10%');
			response.status = 400;
			fee = BOOM_GATE_FEE * 1.1

		# deduct account
		funds = funds - fee;
		update = {
			"$set": {
				"funds": funds
			}
		}

		email = user["email"]
		query = { "email": email }

		db.users.update(query, update)

		# open get
		open_and_close()
		return response.render();


	except Exception as e:
		print(str(e))
		response.set_json_body("Something went wrong. Please try again.");
		response.status = 500;
		return response.render();
