

def pay_for_this_car(request, response):

	# check for authtentication
	user = request.user;

	if (user == None):
		response.status = 400
		response.set_json_body('You need to login in to do this operation');
		return response.render();

	# cheking if the user has enough funds
	email = user["email"]
	db = request.db;
	projection = { "funds": 1, "cars": 1 }
	query = { "email": email }

	number_plate = request.params.get('number_plate');

	user = db.users.find_one(query, projection)

	if (user == None):
		return response.status_500()

	funds = user['funds'];

	if (funds < 10):
		response.status = 500;
		response.set_json_body('You have insufficient funds');
		return response.render();

	# updating

	cars = user['cars'];

	for car in cars:
		if car['number_plate'] == number_plate:
			car['car_license_paid'] = True;


	update = {
		"$set": {
			"cars": cars
		},
		"$inc": {
			"funds": -10 # deducting funds
		}
	}

	db.users.update_one(query, update);

	return response.render();
