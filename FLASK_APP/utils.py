
from db import db
import time
import datetime
from uuid import uuid4
from flask import make_response
import json

# from PIL import Image
import pytesseract
import cv2
# import numpy as np

AUTH_COOKIE_DURATION = 30 * 60;

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



def uuid():
	return str(uuid4())

def auth(request, response):

	try:
		if (request.skip_auth_middleware):
		 	return
	except Exception:
		pass

	request.auth_excecuted = True;
	request.user = None

	cookie = request.cookies.get('auth')
	time = now()

	db = request.db
	query = {
		'auth_cookie': cookie,
		'auth_cookie_expires': {
			'$lt': time
		}
	}

	user = db.users.find_one({ 'auth_cookie': cookie })

	if (user == None):
		request.auth = None
		return;

	email = user['email'];
	is_admin = user['is_admin'];

	# updating cookie
	new_cookie= uuid()
	expires = now() + AUTH_COOKIE_DURATION;

	update = {
		'$set': {
			"auth_cookie": new_cookie,
			"auth_cookie_expires": expires
		}
	}

	query = { 'email': email };
	db.users.update(query, update);

	request.user = { "is_admin": is_admin, "email": email}
	response.set_cookie('auth', new_cookie)


def now():
	return int(time.time())

def currency(amount, sign = ''):
	return sign + "{:,.2f}".format(amount)


def db_middleware(request, response):
	request.db = db
	response.db = db


def date_from_timestamp(timestamp):
	return str(datetime.datetime.fromtimestamp(timestamp))



middlewares = [
	db_middleware,
	auth
]


class HTMLComponent():
	"""docstring for HTMLComponent"""
	def __init__(self, tag, is_container=False):
		self.tag = tag
		self.is_container = is_container
		self.children = []
		self.attributes = {}

	def set_attribute(self, name, value):
		print(self.tag)
		self.attributes[name] = value
		return

	def append(self, node):
		self.children.append(node)

	def render(self):

		tag = self.tag
		children = self.children
		attributes = self.attributes
		is_container = self.is_container

		opening_tag = '<' + tag

		for attr in attributes:
			opening_tag = opening_tag + ' ' + attr + '="' + attributes[attr] + '"'

		opening_tag = opening_tag + '>'

		if (is_container):

			inner_html = ''

			for child in children:
				inner_html =  inner_html + child.render()

			closing_tag = '</' + tag + '>'

			return opening_tag + inner_html + closing_tag

		else:
			return opening_tag

class Response(object):
	"""docstring for Response"""
	def __init__(self, request):
		super(Response, self).__init__()
		self.cookies = {}
		self.headers = {}
		self.body = "OK"
		self.status = 200


		for middleware in middlewares:
			middleware(request, self);

	def set_content_type(self, content_type):
		self.headers['content-type'] = content_type;

	def set_json_body(self, data):
		self.set_content_type('application/json');
		json_str = json.dumps(data);
		self.set_body(json_str)


	def set_body(self, body):
		self.body = body;
		return self;

	def set_cookie(self, cookie, value):
		self.cookies[cookie] = value
		return self

	def set_header(self, header, value):
		self.headers[header] = value;
		return self

	def redirect(self, location):
		self.set_header('location', location)
		self.status = 307
		self.body = "redirect"
		return self.render()

	def redirect_302(self, location):
		self.set_header('location', location)
		self.status = 302
		self.body = "redirect"
		return self.render()

	def status_500(self):
		self.status = 500;
		self.set_body('Something went wrong on our end, please try again');
		return self.render()

	def add_cookies(self, param):

		for key in param:
			self.cookies[key] = param[key];

		return self

	def render(self):

		status = self.status
		body = self.body
		cookies = self.cookies
		headers = self.headers

		response = make_response(body, status)

		for key in cookies:
			response.set_cookie(key, cookies[key])

		for key in headers:
			response.headers[key] = headers[key]

		return response

	def __str__(self):
		return self.render()

