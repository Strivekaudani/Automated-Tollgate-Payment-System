
from flask import render_template
# from passlib.hash import sha256_crypt
from utils import uuid

def create_account(request, response):
	
	name = request.form.get("name")
	surname = request.form.get("surname")
	email = request.form.get("email")
	password = request.form.get("password")
	confirm = request.form.get("confirm")
	car_plate = request.form.get("car_plate"); 

	secure_password = password # sha256_crypt.encrypt(str(password))

	name = name.capitalize()
	surname = surname.capitalize()

	if (car_plate == None):
		response.status = 400;
		return response.redirect_302('/notice?message=You need to own at least one car');


	data = {
		"_id": uuid(),
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

	db = request.db
	db.users.insert_one(data);
	
	return response.redirect_301('/signin')
