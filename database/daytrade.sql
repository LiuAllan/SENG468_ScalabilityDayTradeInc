CREATE TABLE users (
	first_name	VARCHAR(30)		NOT NULL,
	last_name	VARCHAR(30)		NOT NULL,
	account_number	INTEGER		NOT NULL,
	usrname		VARCHAR(20)		UNIQUE NOT NULL,
	password	VARCHAR(30) 	NOT NULL,
	user_id		SERIAL			NOT NULL,
	created		TIMESTAMP 		NOT NULL DEFAULT NOW(),
	
	UNIQUE(username),
);

CREATE TABLE Languages -- Insert manually
(
	user_id		INTEGER		NOT NULL			REFERENCES Users (user_id),
	language	CHAR(3)		UNIQUE NOT NULL -- Three character code according to ISO 631-1
);

CREATE TABLE companies (
	company_id
	company_name	VARCHAR(10)		UNIQUE NOT NULL,
	
);

CREATE TABLE transactions (
	transaction_id		SERIAL NOT NULL,
	
	
	
	transaction_time	TIMESTAMP	NOT NULL  DEFAULT NOW()

);

CREATE TABLE audittrail(
	
);

