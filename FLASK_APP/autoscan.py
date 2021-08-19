
import requests
import os
from time import sleep

# os.system('clear')
# print("AUTOGATE: autodetect started...")


class Global(object):
	prev_plate = None

glob = Global();

sleep(5)

while (True):

	url = 'http://localhost:5000/api/auto-scan-command';
	prev_plate = glob.prev_plate;

	if (prev_plate):
		# print('glob.prev_plate:', prev_plate);
		url = url + '?prev_plate=' + prev_plate;

	try:

		response = requests.post(url);
		data = response.json()
		number_plate = data.get('number_plate');

		if (number_plate):
			glob.prev_plate = number_plate
			# print("glob.prev_plate set to:", number_plate);

		# print(data.get('message'))

	except Exception as e:
		# print(str(e))
		pass
