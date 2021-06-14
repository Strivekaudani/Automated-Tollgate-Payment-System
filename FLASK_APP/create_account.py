
from flask import render_template
from passlib.hash import sha256_crypt
from utils import uuid

def create_account(request, response):
	
	name = request.form.get("name")
	surname = request.form.get("surname")
	email = request.form.get("email").lower()
	password = request.form.get("password")
	confirm = request.form.get("confirm")
	car_plate = request.form.get("car_plate").upper(); 

	secure_password = sha256_crypt.encrypt(str(password))

	name = name.capitalize()
	surname = surname.capitalize()

	if (car_plate == None):
		return response.redirect_302('/notice?message=You need to own at least one car');


	# check if email is already used	
	db = request.db
	query = { "email": email }
	projection = { "_id": 1 }
	user = db.users.find_one(query, projection);

	if user != None:
		return response.redirect_302('/notice?message=The email is already being used');



	data = {
		"name": name,
		"surname": surname,
		"email": email,
		"password": secure_password,
		"is_admin": False,
		"funds": 0,
		"cars": [
			{
				"number_plate": car_plate,
				"car_license_paid": False
			},
		]
	}

	db.users.insert_one(data);
	
	return response.redirect_302('/signin')
