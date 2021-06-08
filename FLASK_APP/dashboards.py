
from utils import currency , HTMLComponent
from flask import render_template, make_response

def user_dashboard(request, response):

	user = request.user;
	if user == None:
		return response.redirect_302('/notice?message=You need to login to access this page.');

	email = user["email"]

	# get car info
	db = request.db
	query = { "email": email }
	projection = { "cars": 1, "funds": 1, "name": 1, "surname": 1}

	user = db.users.find_one(query, projection)
	cars = user['cars']
	funds = user['funds']
	funds = currency(funds, '$');

	body = render_template('user-dashboard.html', cars=cars, funds=funds)
	response.set_body(body)

	return response.render();


def admin_dashboard(request, response):
	
	# auth
	user = request.user;

	print (user)

	if (user == None):
		return response.redirect_302('/notice?message=You need to login to access this page.');

	is_admin = user['is_admin'];

	if (not is_admin):
		return response.redirect_302('/notice?message=You are not authorized to access this page.');

	# getting data
	## getting dpayments
	db = request.db;

	payments = list(db.payments.find({}));
	print(payments);
	projection = { "name": 1, "surname": 1 }

	for payment in payments:

		# getting user name
		email = payment['email'];
		query = { 'email': email }
		depositer = db.users.find_one(query, projection);

		payment["depositer"] = depositer;

		print(payment)


	body = render_template('admin-dashboard.html', payments=payments);
	response.set_body(body)

	return response.render();





