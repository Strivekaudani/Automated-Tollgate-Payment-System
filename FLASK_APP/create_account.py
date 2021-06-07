
from flask import render_template
# from passlib.hash import sha256_crypt

def create_account(request, response, db):
	
	name = request.form.get("name")
	surname = request.form.get("surname")
	email = request.form.get("email")
	password = request.form.get("password")
	confirm = request.form.get("confirm")
	car_plate = request.form.get("car_plate"); 

	secure_password = password # sha256_crypt.encrypt(str(password))

	name = name.capitalize()
	surname = surname.capitalize()


	sql = "INSERT INTO users (name, surname, email, password, is_admin, funds) VALUES(:name, :surname, :email, :password, :is_admin, :funds)"
	data = {
		"name": name,
		"surname": surname,
		"email": email,
		"password": secure_password,
		"is_admin": True,
		"funds": 0
	}

	db.execute(sql, data);
	db.commit()

	return render_template('welcome.html', nm = name, funds = 0, license = "null")
