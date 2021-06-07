
from db import db
import time
from uuid import uuid4
from flask import make_response

AUTH_COOKIE_DURATION = 30 * 60;




class Response(object):
	"""docstring for Response"""
	def __init__(self, request):
		super(Response, self).__init__()
		self.cookies = {}
		self.headers = {}
		self.body = ""
		self.status = 200

		for middleware in middlewares:
			middleware(request, self);

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

	sql = 'SELECT email,  is_admin FROM users WHERE auth_cookie=:cookie AND auth_cookie_expires>:_time';
	data = { "cookie": cookie, "_time": time }

	user = db.execute(sql, data).fetchone()

	if (user == None):
		request.auth = None
		return;

	email = user[0];
	is_admin = user[1];

	# updating cookie
	new_cookie= uuid()
	expires = now() + AUTH_COOKIE_DURATION;

	sql = 'UPDATE users SET auth_cookie=:new_cookie, auth_cookie_expires=:expires WHERE email=:email'
	data = {
		"new_cookie": new_cookie,
		"email": email,
		"expires": expires
	}


	db.execute(sql, data)
	db.commit()

	request.user = { "is_admin": is_admin, "email": email}
	response.set_cookie('auth', new_cookie)


def now():
	return int(time.time())

def currency(amount, sign = ''):
	return sign + "${:,.2f}"


def db_middleware(request, response):
	request.db = db
	response.db = db


middlewares = [
	auth,
	db_middleware
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
