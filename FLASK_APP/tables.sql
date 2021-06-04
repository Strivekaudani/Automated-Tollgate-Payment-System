
CREATE TABLE users (
	name VARCHAR(50),
	surname VARCHAR(50),
	email VARCHAR(50) PRIMARY KEY,
	password VARCHAR(255),
	is_admin BOOLEAN,
	funds REAL(10,2),
	auth_cookie VARCHAR(100),
	auth_cookie_expires INT
);

CREATE TABLE cars (
	number_plate VARCHAR(20) PRIMARY KEY,
	car_license_paid BOOLEAN
);

CREATE TABLE temporary_funds (
	email VARCHAR(100),
	time DATETIME,
	amount REAL(10, 2),
	verification_code TEXT
);

INSERT INTO users (name, surname, email, password, is_admin, funds) VALUES (
				'CLAYTON', 'SIBANDA', 'claytonsibanda@gmail.com', '$5$rounds=535000$JYWmOUjc4gL86LW5$ygmgXXn5xU9fYdHFVx4ujHHDbbY.ccUp0Sq4JWoRGg.', true, 0
);