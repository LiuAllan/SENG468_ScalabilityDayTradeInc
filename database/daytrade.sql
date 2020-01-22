CREATE EXTENSION pgcrypto;

CREATE TABLE Users (
	user_id		SERIAL			NOT NULL PRIMARY KEY,
	first_name	VARCHAR(30)		NOT NULL,
	last_name	VARCHAR(30)		NOT NULL,
	account_num	INTEGER			NOT NULL,
	username	VARCHAR(20)		UNIQUE NOT NULL,
	password	VARCHAR(30) 	NOT NULL,
	created		TIMESTAMP 		NOT NULL DEFAULT NOW(),
	
	UNIQUE(username),
);

CREATE TABLE AddAmount(
	id			INTEGER		NOT NULL 	REFERENCES Users (user_id),
	amount		INTEGER		NOT NULL
);

CREATE TABLE Buy(
	id			INTEGER		NOT NULL 	REFERENCES Users (user_id),
	amount		INTEGER		NOT NULL
);

CREATE TABLE Companies (
	company_id		SERIAL			NOT NULL PRIMARY KEY,
	company_name	VARCHAR(10)		UNIQUE NOT NULL,
);

CREATE TABLE Transactions (
	id					INTEGER		NOT NULL REFERENCES Users (user_id
	transaction_id		SERIAL		NOT NULL,
	
	
	
	
	transaction_time	TIMESTAMP	NOT NULL  DEFAULT NOW()

);

CREATE TABLE AuditTrail(
	
);

CREATE FUNCTION create_user(
	first_name		VARCHAR(30),
	last_name		VARCHAR(30),
	account_num		INTEGER,
	_username		VARCHAR(20),
	password		VARCHAR(30)
)
RETURNS void
LANGUAGE plpgsql
as $$
BEGIN
	INSERT INTO Users (first_name, last_name, account_num,
		username, password)
	VALUES (first_name, last_name, account_num, _username,
			crypt(password, gen_salt('bf')));
END;
$$;

CREATE FUNCTION audit_log()
RETURNS void
LANGUAGE plpgsql
as $$
BEGIN
	SELECT * FROM 
END;
$$;