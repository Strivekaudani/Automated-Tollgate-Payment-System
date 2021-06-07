
from utils import auth
from flask import render_template, make_response

def user_dashboard(request, response, db):

	# authenticate request
	auth(request, response)

	user = request.user;
	if user == None:
		return render_template('error.html', error_msg = 'You need to login to access this page')

	email = user["email"]

	# get car info
	sql = 'SELECT number_plate, is_car_license_paid FROM cars WHERE owner_email=:email'
	data = { "email": email }

	cars = db.execute(sql, data).fetchmany()

	return "User dashboard";


def admin_dashboard(request, response):
	pass

