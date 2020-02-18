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
  stock_sym varchar(3) NOT NULL,
  amount int NOT NULL,	--whole number of stocks to buy/sell
  funds int NOT NULL,	--money used to buy/sell stock
  timeadded bigint NOT NULL,

  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE BuyTriggers (
  user_id varchar(30) NOT NULL,
  stock_sym varchar(3) NOT NULL,
  reserve int NOT NULL,	--funds taking from user
  trigger_amount int NOT NULL,	--amount to trigger at

  UNIQUE(user_id, stock_sym)
  --FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE SellTriggers (
  user_id varchar(30) NOT NULL,
  stock_sym varchar(3) NOT NULL,
  amount int NOT NULL,	--dollar amount to sell
  reserve int NOT NULL,	--shares taking from account
  trigger_amount int NOT NULL,	--amount to trigger at

  UNIQUE(user_id, stock_sym)
  --FOREIGN KEY (user_id) REFERENCES Users (user_id)
);

CREATE TABLE Audit (
  audit_id serial,
  user_id varchar(30) NOT NULL,
  command varchar(30),
  timeadded bigint NOT NULL,
  stock_sym varchar(3),
  amount int,
  funds int,
  cryptokey varchar(100),
  server varchar(30) NOT NULL,
  filename varchar(30),
  stock_price int,
  quote_time bigint,
  action varchar(30),
  error_msg varchar(100),
  debug_msg varchar(100),

  PRIMARY KEY (audit_id),
  FOREIGN KEY (user_id) REFERENCES Users (user_id)
);
