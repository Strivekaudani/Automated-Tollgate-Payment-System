
from flask import render_template
from passlib.hash import sha256_crypt
from utils import uuid
from flask_mail import Message;


def create_account(request, response, mail):
	
	name = request.form.get("name")
	surname = request.form.get("surname")
	email = request.form.get("email").lower()
	password = request.form.get("password")
	confirm = request.form.get("confirm")
	car_plate = request.form.get("car_plate").upper();
	car_type = request.form.get('car_type');

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
				"car_license_paid": False,
				"car_type": car_type
			},
		]
	}

	db.users.insert_one(data);

	try:

		email_message = Message('Welcome', sender="Autogate <autogate@gmail.com>", recipients=[ email ]) 
		email_message.body = f'Thank you for creating an account with us. Proceed to sign in.';
		mail.send(email_message);

	except:
		pass

	return response.redirect_302('/signin')
