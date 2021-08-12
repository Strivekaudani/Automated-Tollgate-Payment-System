
from flask import render_template
from utils import uuid, now, get_ip_as_seen_by
from modded_paynow import Paynow

PAYNOW_ID = '11223';
PAYNOW_API_KEY = 'aff446cf-4618-4f92-a780-41662ec699fb';

# def add_funds(request, response):

# 	# check authentication
# 	user = request.user;

# 	if (user == None):
# 		return response.redirect_302('/notice?message=You need to login to add funds')

# 	# extracting data
# 	amount = request.form.get('amount');
# 	verification_code = request.form.get('verification_code');

# 	# adding data to database
# 	db = request.db;

# 	data = {
# 		"email": user["email"],
# 		'_id': uuid(),
# 		"amount": amount,
# 		"verification_code": verification_code,
# 		"time": now()
# 	}

# 	db.payments.insert_one(data);

# 	return response.redirect_302('/notice?message=Your funds are waiting approval')


def add_funds(request, response, mail, Message):

	try:

		# check authentication
		user = request.user;

		if (user == None):
			return response.redirect_302('/notice?message=You need to login to add funds')

		# extracting data
		amount = request.form.get('amount');
		email = user['email'];
		ref_code = uuid()

		ip_address = get_ip_as_seen_by(request.remote_addr);
		return_url = 'http://' + ip_address + ':5000/poll-payment?ref_code=' + ref_code;
		result_url = 'http://localhost';
		paynow = Paynow(PAYNOW_ID, PAYNOW_API_KEY, return_url, result_url);

		payment = paynow.create_payment(ref_code, email)
		payment.add('Add funds to Autogate Account', amount);

		payment_response = paynow.send(payment)

		if (payment_response.success == False):
			return response.redirect_302('/notice?message=Something went wrong. Try again')

		payment_link = payment_response.redirect_url;
		poll_url = payment_response.poll_url

		# adding data to database
		db = request.db;

		data = {
			"email": user["email"],
			'_id': uuid(),
			"amount": amount,
			"ref_code": ref_code,
			"time": now(),
			"poll_url": poll_url
		}

		db.payments.insert_one(data);

		return response.redirect_302(payment_link);

	except Exception as e:
		print(str(e))
		return response.redirect_302('/notice?message=Something went wrong. Try again');


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

def poll_payment(request, response, mail, Message):

	ref_code = request.args.get('ref_code');

	## getting poll url
	db = request.db
	query = { 'ref_code': ref_code };
	payment = db.payments.find_one(query);

	if (payment == None):
		return response.redirect_302('/notice?message=Invalid ref code')


	# polling the payment
	poll_url = payment['poll_url'];
	paynow = Paynow(PAYNOW_ID, PAYNOW_API_KEY, 'http://localhost', 'http://localhost');
	status = paynow.check_transaction_status(poll_url);
	is_paid = status.paid;

	email = payment["email"];
	amount = payment["amount"];

	if (not is_paid):

		try:
			email_message = Message('You cancelled your payment', sender="Autogate <autogate@gmail.com>", recipients=[ email ]) 
			email_message.body = f'You cancelled your payment of ${amount}.';
			mail.send(email_message);
			return response.redirect_302('/notice?message=You cancelled your payment');
		except:
			pass

	## incrementing funds in the user's account
	query = { "email": email }
	update = {
		"$inc": {
			"funds": float(amount)
		}
	}


	db.users.update(query, update);

	## deleting payment
	query = {"ref_code": ref_code }
	db.payments.delete_one(query)

	# recording the transaction
	## get user name and surname
	projection = { 'surname': 1, 'name': 1, 'funds': 1 }
	query = { 'email': email}

	user = db.users.find_one(query, projection) or { 'name': 'Username', 'surname': ''};
	name = user['name'];
	surname = user['surname'];

	## inserting data
	db.transactions.insert_one({
		'type': 'ACCOUNT_TOPUP',
		'amount': float(amount),
		'done_by': f'{name} {surname}',
		'time': now(),
		'notes': f'{name} {surname} topped their account by ${amount}'
	});

	balance = user['funds'];

	try:
		email_message = Message('Account Topup', sender="Autogate <autogate@gmail.com>", recipients=[ email ]) 
		email_message.body = f'You topped up your with ${amount}. Your balance is now ${balance}';
		mail.send(email_message);
	except:
		pass

	return response.redirect_302('/notice?message=Your payment was successful')


def visitor_payment(request, response):

	# authentication
	user = request.user
	if (user == None):
		return response.redirect_302('/notice?message=You need to login to make this operation')

	is_admin = user['is_admin']
	if (not is_admin):
		return response.redirect_302('/notice?message=You are not authorized to do this');







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


