import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Database:

    def __init__(self):
        # connecting to generic user
        self.conn = psycopg2.connect("dbname=postgres host=localhost user=postgres password=postgres")
        self.cur = self.conn.cursor()
        file = open("DBInit.sql", "r")
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        # Set Database and user
        for line in file:
            print(line)
            self.cur.execute(line)
        file.close()
        self.cur.close()
        self.conn.close()
        # connecting to seng468 user
        self.conn = psycopg2.connect("dbname=daytrading user=seng468 password='seng468'")
        self.cur = self.conn.cursor()
        file = open("daytrading.sql", "r")
        # Set up tables
        self.cur.execute(file.read())
        file.close()


    def close(self):
        self.cur.close()
        self.conn.close()


    # Input: the user_id of the record
    # Output: a tuple containing (user_id, funds)
    # If no record is found returns None
    def selectUsers(self, user_id):
        self.cur.execute("""
	    Select *
	    From users
	    Where user_id = '{}';
	    """.format(user_id))

        result = self.cur.fetchone()

        #print(result)

        return result


    # Input: the user_id and the stock_sym of the record
    # Output: a tuple containing (user_id, stock_sym, amount)
    # If no record is found returns None
    def selectAccount(self, user_id, stock_sym):
        self.cur.execute("""
	    Select *
    	From account
	    Where user_id = '{}' and stock_sym = '{}';
    	""".format(user_id, stock_sym))

        result = self.cur.fetchone()

        #print(result)

        return result


    # Input: the user_id, command, and the stock_sym of the record
    # Output: a tuple containing (user_id, command, stock_sym, amount, funds, timeadded) with highest timeadded (most recent)
    # If no record is found returns None
    def selectPending(self, user_id, command, stock_sym):
        self.cur.execute("""
	    Select *
	    From pending
	    Where user_id = '{}' and command = '{}' and stock_sym = '{}'
	    Order By timeadded desc
	    limit 1;
	    """.format(user_id, command, stock_sym))

        result = self.cur.fetchone()

        #print(result)

        return result


    # Input: the user_id and funds
    # Output: good
    # The record containing user_id has it's funds changed to input funds
    # If no record is found creates a record with user_id and funds
    def changeUsers(self, user_id, funds):
        self.cur.execute("""
        INSERT INTO Users
        Values
        (
          '{}', --user_id
          {}    --funds
        )
        On Conflict (user_id)
        DO
        Update
        SET funds = {};
        """.format(user_id, funds, funds))

        #result =self.cur.fetchone()

        #print('good')

        return 'good'


    # Input: the user_id, stock_sym, and amount
    # Output: good
    # The record containing user_id and stock_sym has it's amount changed to input amount
    # If no record is found creates a record with user_id, stock_sym and amount
    def changeAccount(self, user_id, stock_sym, amount):
        self.cur.execute("""
        INSERT INTO Account
        Values
        (
          '{}', --user_id
          '{}', --stock_sym
          {}    --amount
        )
        On Conflict (user_id, stock_sym)
        DO
        Update
        SET amount = {};
        """.format(user_id, stock_sym, amount, amount))

        #result =self.cur.fetchone()

        #print('good')

        return 'good'


    # Input: the user_id, command, stock_sym, amount, funds, and timeadded
    # Output: good
    # Inserts a new record with user_id, command, stock_sym, amount, funds, and timeadded
    def addPending(self, user_id, command, stock_sym, amount, funds, timeadded):
        self.cur.execute("""
        INSERT INTO Pending
        Values
        (
          '{}', --user_id
          '{}', --command
          '{}', --stock_sym
          {},   --amount
          {},   --funds
          {}    --timeadded
        );
        """.format(user_id, command, stock_sym, amount, funds, timeadded))

        #result =self.cur.fetchone()

        #print('good')

        return 'good'


    # Input: the user_id, command, stock_sym
    # Output: bad
    # Delete the record with user_id, command, stock_symwith highest timeadded (most recent)
    def removePending(self, user_id, command, stock_sym):
        self.cur.execute("""
        Delete
        From Pending
        Where ctid --implicit line id
        In (
        Select ctid
        From Pending
        Where user_id = '{}' and command = '{}' and stock_sym = '{}'
        Order By timeadded desc
        limit 1
        );
        """.format(user_id, command, stock_sym))

        #result = self.cur.fetchone()

        #print(result)

        return 'bad'
