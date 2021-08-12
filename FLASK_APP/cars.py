

def pay_for_car(request, response):

	try:

		# check for authtentication
		user = request.user;

		if (user == None):
			return response.redirect_302('/notice?message=You need to login in to do this operation');

		# cheking if the user has enough funds
		email = user["email"]
		db = request.db;
		projection = { "funds": 1, "cars": 1 }
		query = { "email": email }

		number_plate = request.form.get('number_plate');

		user = db.users.find_one(query, projection)

		if (user == None):
			return response.redirect_302('/notice?message=SOMETHING WENT WRONG ON OUR END');

		funds = user['funds'];

		if (funds < 10):
			return response.redirect_302('/notice?message=INSUFFICIENT FUNDS');

		# updating
		cars = user['cars'];

		for car in cars:
			if car['number_plate'] == number_plate:
				car['car_license_paid'] = True;

		funds = funds - 10;

		update = {
			"$set": {
				"cars": cars,
				"funds": funds
			}
		}

		db.users.update_one(query, update);

		return response.redirect_302('/user-dashboard');

	except Exception as e:
		error_msg = str(e)
		print('ERROR: ', error_msg)
		return response.status_500()

def add_car(request, response):
	
	# authentication
	user = request.user;

	if (user == None):
		response.status = 400
		return response.redirect_302('/notice?message=You need to login in to do this operation');

	# add car
	number_plate = request.form.get('number_plate').upper();
	car_type = request.form.get('car_type');
	email = user["email"];

	car = {
		"number_plate": number_plate,
		"car_license_paid": False,
		"car_type": car_type
	}

	update = {
		"$push": {
			"cars": car
		}
	}

	db = response.db
	query = { "email": email }
	db.users.update(query, update);

	return response.redirect_302('/user-dashboard');


def remove_car(request, response):
	
	# authentication
	user = request.user;

	if (user == None):
		response.status = 400
		return response.redirect_302('/notice?message=You need to login in to do this operation');

	# checking if car is paid
	db = request.db
	email = user['email']
	number_plate = request.form.get('number_plate');

	query = { "email": email }
	projection = { "cars": 1 }

	user = db.users.find_one(query, projection)
	cars = user['cars']
	cars_left = []

	for car in cars:

		if (car["number_plate"] == number_plate):

			if (car['car_license_paid']):
				continue
			else:
				return response.redirect_302('/notice?message=You cannot remove an unpaid car')

		cars_left.append(car)


	update = {
		'$set': {
			"cars": cars_left
		}
	}

	db.users.update_one(query, update)
	return response.redirect_302('/user-dashboard');
