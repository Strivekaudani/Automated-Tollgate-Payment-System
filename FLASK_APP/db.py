

from pymongo import MongoClient
from passlib.hash import sha256_crypt


client = MongoClient('mongodb://localhost:27017');
db = client['autogate']


data = {
	"name": 'CLAYTON',
	'surname': 'SIBANDA',
	'email': 'claytonsibanda@gmail.com',
	'password': sha256_crypt.encrypt('admin'),
	'is_admin': True,
	'funds': 0,
	'cars': []
}

try:

	users_count = db.users.count();
	
	if users_count == 0:
		db.users.insert_one(data);

except Exception as e:
	print(str(e))