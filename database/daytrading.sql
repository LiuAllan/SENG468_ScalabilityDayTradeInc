CREATE TABLE Users (
  user_id varchar(30) NOT NULL,
  funds int NOT NULL,

  PRIMARY KEY (user_id)
);

CREATE TABLE Account (
  user_id varchar(30) NOT NULL,
  stock_sym varchar(3) NOT NULL,
  amount int NOT NULL,

  PRIMARY KEY (user_id, stock_sym),
  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE Pending (
  user_id varchar(30) NOT NULL,
  command varchar(30) NOT NULL,
  stock_sym varchar(3),
  amount int,
  timeadded timestamp NOT NULL,

  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE Audit (
  audit_id serial,
  user_id varchar(30) NOT NULL,
  command varchar(30) NOT NULL,
  funds int,
  stock_sym varchar(3),
  amount int,
  timeadded timestamp NOT NULL,
  cryptokey int,

  PRIMARY KEY (audit_id),
  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE OR REPLACE FUNCTION clean (timenow timestamp)
  RETURNS boolean as true
  BEGIN
    DELETE FROM Pending
      WHERE (timenow - 60000 <= timeadded) --pending time past 60 sec
  END;
  LANGUAGE plpgsql;

--Select funds (user)
CREATE OR REPLACE FUNCTION selectFund (user varchar(30))
  RETURNS int as $fund$
  DECLARE
    fund int;
  BEGIN
    Select funds into fund from users where user_id = user;
    Return fund;
  END;
  LANGUAGE plpgsql;

--Change funds (user, funds), if needed create row with user, fund
CREATE OR REPLACE FUNCTION changeFund (user varchar(30), fund int)
  RETURNS boolean as true
  BEGIN
    INSERT INTO Users (user_id, funds)--create new row
      Values
        (
          user,
          fund
        )
    On Conflict (user_id) --if row already exists
      DO
        Update
         SET funds = fund --change funds
  END;
  LANGUAGE plpgsql;


--Select amount (user, stock)
CREATE OR REPLACE FUNCTION selectAmount (user varchar(30), stock varchar(3))
  RETURNS int as $amountOfStock$
  DECLARE
    amountOfStock int;
  BEGIN
    Select amount into amountOfStock from Account where user_id = user and stock_sym = stock;
    Return amountOfStock;
  END;
  LANGUAGE plpgsql;

--Change amount (user, stock, amount), if needed create row with user, stock, amount
CREATE OR REPLACE FUNCTION changeFund (user varchar(30), stock varchar(3), amountOfStock int)
  RETURNS boolean as true
  BEGIN
    INSERT INTO Account (user_id, stock_sym, amount)--create new row
      Values
        (
          user,
          stock,
          amountOfStock
        )
    On Conflict (user_id, stock_sym) --if row already exists
      DO
        Update
         SET amount = amountOfStock --change funds
  END;
  LANGUAGE plpgsql;
