CREATE TABLE IF NOT EXISTS users (userid INTEGER NOT NULL, username CHAR(8), firstname VARCHAR(30), lastname VARCHAR(30), city VARCHAR(30), state CHAR(2), email VARCHAR(100),phone CHAR(14), numberofdocuments INTEGER);

LOAD DATA INFILE 'users.csv'
INTO TABLE users
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(usersid, username, firstname, lastname, city, state, email, phone, numberofdocuments);
