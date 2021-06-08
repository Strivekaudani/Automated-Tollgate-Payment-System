
from flask import render_template
from utils import uuid, now

def add_funds(request, response):

	# check authentication
	user = request.user;

	if (user == None):
		return response.redirect_302('/notice?message=You need to login to add funds')

	# extracting data
	amount = request.form.get('amount');
	verification_code = request.form.get('verification_code');

	# adding data to database
	db = request.db;

	data = {
		"email": user["email"],
		'_id': uuid(),
		"amount": amount,
		"verification_code": verification_code,
		"time": now()
	}

	db.payments.insert_one(data);

	return response.redirect_302('/notice?message=Your funds are waiting approval')


def approve_funds(request, response):

	# auth
	user = request.user;

	if (user == None):
		return response.redirect_302('/notice?message=You need to login to make this operation')

	is_admin = user['is_admin']
	if (not is_admin):
		return response.redirect_302('/notice?message=You are not authorized to do this');

	# extracting data
	_id = request.form.get('payment_id');

	# approving
	## getting payment data
	db = request.db
	query = { '_id': _id };
	payment = db.payments.find_one(query)

	## incrementing funds in the user's account
	amount = payment["amount"];
	email = payment["email"];
	query = { "email": email }
	update = {
		"$inc": {
			"funds": float(amount)
		}
	}


	db.users.update(query, update);

	## deleting payment
	query = {"_id": _id }
	db.payments.delete_one(query)

	return response.redirect_302('/admin-dashboard');


def remove_payment(request, response):
	
	# authentication
	user = request.user
	if (user == None):
		return response.redirect_302('/notice?message=You need to login to make this operation')

	is_admin = user['is_admin']
	if (not is_admin):
		return response.redirect_302('/notice?message=You are not authorized to do this');


	# remove payment
	_id = request.form.get('payment_id');
	db = request.db;
	query = { "_id": _id }
	db.payments.delete_one(query) 

	return response.redirect_302('/admin-dashboard');


