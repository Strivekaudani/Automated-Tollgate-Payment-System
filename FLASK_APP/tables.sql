
CREATE TABLE users (
	name VARCHAR(50),
	surname VARCHAR(50),
	email VARCHAR(50) PRIMARY KEY,
	password VARCHAR(255),
	is_admin INT,
	funds REAL(10,2),
	auth_cookie VARCHAR(100),
	auth_cookie_expires INT
);

CREATE TABLE cars (
	owner_email VARCHAR(100),
	number_plate VARCHAR(20) PRIMARY KEY,
	is_car_license_paid BOOLEAN
);

CREATE TABLE temporary_funds (
	email VARCHAR(100),
	time DATETIME,
	amount REAL(10, 2),
	verification_code TEXT
);
