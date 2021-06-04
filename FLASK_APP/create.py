
from db import db

# reading sql file
f = open("tables.sql", 'r');
contents = f.read();

statements = contents.split(';');

# executing sql statements
for statement in statements:

	statement = statement.strip();

	if (statement == ''):
		continue

	statement = statement.replace('\r\n', ' ')
	statement = statement.replace('\n\r', ' ')
	statement = statement.replace('\n', ' ')
	statement = statement.replace('\r', ' ')

	try:
		db.execute(statement);
	except Exception as e:
		print(statement);
		print (str(e))




