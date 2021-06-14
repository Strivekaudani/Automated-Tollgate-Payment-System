
from flask import render_template, make_response
from passlib.hash import sha256_crypt
from utils import uuid, now
from constants import AUTH_TOKEN_VALIDITY_DURATION

def sign_in(request, response):

	# extracting posted data
	email = request.form["email"].lower();
	password = request.form["password"]

	# validating credentials
	query = { "email": email }
	db = request.db

	user = db.users.find_one(query);

	if user == None:
		return response.redirect_302('/notice?message=Invalid credentials')

	is_password_valid = sha256_crypt.verify(password, user['password'])
	if not is_password_valid:
		return response.redirect_302('/notice?message=Invalid credentials')

	# auth cookie
	## setting cookie
	auth_cookie = uuid()
	response.set_cookie('auth', auth_cookie)

	## storing cookie in the database
	update = {
		'$set': {
			"auth_cookie": auth_cookie,
			"auth_cookie_expires": now() + AUTH_TOKEN_VALIDITY_DURATION
		}
	}

	db.users.update(query, update)

	# select which dashboard to render, based on the account type
	is_admin = user['is_admin'];

	if (is_admin):
		return response.redirect_302('/admin-dashboard')
	else:
		return response.redirect_302('/user-dashboard');


