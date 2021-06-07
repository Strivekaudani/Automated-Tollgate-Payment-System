
from flask import render_template, make_response
# from passlib.hash import sha256_crypt
from utils import uuid, now
from constants import AUTH_TOKEN_VALIDITY_DURATION

def sign_in(request, response, db):

	# extracting posted data
	email = request.form["email"];
	password = request.form["password"]

	# validating credentials
	sql = 'SELECT password, is_admin FROM users WHERE email=:email'
	data = { "email": email }
	user = db.execute(sql, data).fetchone()

	if user == None:
		return render_template('error.html', error_msg = "Invalid credentials")

	if user[0] != password:
		return render_template('error.html', error_msg = "Invalid credentials")

	# auth cookie
	## setting cookie
	auth_cookie = uuid()
	response.set_cookie('auth', auth_cookie)

	## storing cookie in the database
	sql = 'UPDATE users SET auth_cookie=:auth_cookie, auth_cookie_expires=:auth_cookie_expires WHERE email=:email'
	data = {
		"email": email,
		"auth_cookie": auth_cookie,
		"auth_cookie_expires": now() + AUTH_TOKEN_VALIDITY_DURATION
	}

	db.execute(sql, data)
	db.commit()

	request.skip_auth_middleware = True

	# select which dashboard to render, based on the account type
	is_admin = user[1];

	if (is_admin):
		return response.redirect('/admin-dashboard')
	else:
		return response.redirect('/user-dashboard');


