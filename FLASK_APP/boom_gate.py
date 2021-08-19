
try:
	import pigpio
except:
	import fake_pigpio as pigpio
	
from time import sleep
from utils import now

pi = pigpio.pi()
SERVO = 17
OPEN_WINDOW = 5; # 5 SECONDS
MIN_PW = 1000
MID_PW = 1500
MAX_PW = 2000

def open_gate():
	pi.set_servo_pulsewidth(SERVO, MAX_PW)

def close_gate():
	pi.set_servo_pulsewidth(SERVO, MIN_PW)

def open_and_close():
	open_gate();
	sleep(OPEN_WINDOW);
	close_gate();

def open_gate_handler(request, response):

	# auth
	user = request.user;

	if (user == None):
		response.set_json_body('You need to login to open the gate');
		response.status = 401;
		return response.render();

	is_not_admin = not user["is_admin"];

	if (is_not_admin):
		response.set_json_body('You are not authorized to open the gate');
		response.status = 403
		return response.render();


	# record transaction

	if (request.args.get('amount')):
		amount = float(request.args.get('amount'))
		number_plate = request.args.get('number_plate') or '<no_number_plate>';

		db = request.db;

		db.transactions.insert_one({
			'type': 'TOLL_FEE_PAYMENT',
			'amount': amount,
			'done_by': f'MANUAL_PAYMENT',
			'time': now(),
			'notes': f'Car {number_plate} paid a toll fee of ${amount}'
		});

	# open the gate
	open_and_close();
	response.set_json_body('OK')
	return response.render();

close_gate();
sleep(3)
