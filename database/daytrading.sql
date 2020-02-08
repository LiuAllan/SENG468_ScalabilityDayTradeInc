CREATE TABLE Users (
  user_id varchar(30) NOT NULL,
  funds int NOT NULL,	--money user has

  PRIMARY KEY (user_id)
);

CREATE TABLE Account (
  user_id varchar(30) NOT NULL,
  stock_sym varchar(3) NOT NULL,
  amount int NOT NULL,	--whole number of stock user has

  PRIMARY KEY (user_id, stock_sym),
  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE Pending (
  user_id varchar(30) NOT NULL,
  command varchar(30) NOT NULL,	--buy/sell
  stock_sym varchar(3),
  amount int,	--whole number of stocks to buy/sell
  funds int,	--money used to buy/sell stock
  timeadded bigint NOT NULL,

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
