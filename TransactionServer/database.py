import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Database:

    def __init__(self):
        # Connecting to generic user
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
        # Connecting to seng468 user
        self.conn = psycopg2.connect("dbname=daytrading user=seng468 password='seng468'")
        self.cur = self.conn.cursor()
        file = open("daytrading.sql", "r")
        # Set up tables
        self.cur.execute(file.read())
        file.close()


    def close(self):
        self.cur.close()
        self.conn.close()


    ##
    ## Users Table
    ##

    # Input: (user_id)
    # Output: (user_id, funds)
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

    # Input: (user_id, funds)
    # Output: The record that is created/updated
    # The record containing user_id has it's funds changed to input funds
    # If no record is found creates a record with user_id and funds
    def changeUsers(self, user_id, funds):
        self.cur.execute("""
        INSERT INTO Users
        Values
        (
          '{0}', --user_id
          {1}    --funds
        )
        On Conflict (user_id)
        DO
        Update
        SET funds = {1}
        Returning *;
        """.format(user_id, funds))

        result = self.cur.fetchone()

        #print('good')

        return result


    ##
    ## Accounts Table
    ##

    # Input: (user_id, stock_sym)
    # Output: (user_id, stock_sym, amount)
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

    # Input: (user_id, stock_sym, amount)
    # Output: The record that is created/updated
    # The record containing user_id and stock_sym has it's amount changed to input amount
    # If no record is found creates a record with user_id, stock_sym and amount
    def changeAccount(self, user_id, stock_sym, amount):
        self.cur.execute("""
        INSERT INTO Account
        Values
        (
          '{0}', --user_id
          '{1}', --stock_sym
          {2}    --amount
        )
        On Conflict (user_id, stock_sym)
        DO
        Update
        SET amount = {2}
        Returning *;
        """.format(user_id, stock_sym, amount))

        result = self.cur.fetchone()

        #print('good')

        return result


    ##
    ## Pending Table
    ##

    # Input: (user_id, command)
    # Output: (user_id, command, stock_sym, amount, funds, timeadded) with highest timeadded (most recent)
    # If no record is found returns None
    def selectPending(self, user_id, command):
        self.cur.execute("""
	    Select *
	    From pending
	    Where user_id = '{}' and command = '{}'
	    Order By timeadded desc
	    limit 1;
	    """.format(user_id, command))

        result = self.cur.fetchone()

        #print(result)

        return result

    # Input: (user_id, command, stock_sym, amount, funds, timeadded)
    # Output: The record that is created
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
        )
        Returning *;
        """.format(user_id, command, stock_sym, amount, funds, timeadded))

        result = self.cur.fetchone()

        #print('good')

        return result

    # Input: (user_id, command)
    # Output: The record that is deleted
    # Delete the record with user_id, command with highest timeadded (most recent)
    def removePending(self, user_id, command):
        self.cur.execute("""
        Delete
        From Pending
        Where ctid --implicit line id
        In (
        Select ctid
        From Pending
        Where user_id = '{}' and command = '{}'
        Order By timeadded desc
        limit 1
        )
        Returning *;
        """.format(user_id, command))

        result = self.cur.fetchone()

        #print(result)

        return result


    ##
    ## Triggers
    ## In Pending Table

    # Input: (user_id, command, stock_sym)
    # Output: (user_id, command, stock_sym, amount, funds, timeadded)
    # If no record is found returns None
    def selectTrigger(self, user_id, command, stock_sym):
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

    # Input: (user_id, command, stock_sym, amount, funds, timeadded)
    # Output: The record that is created
    # Inserts a new record with user_id, command, stock_sym, amount, funds, and timeadded
    def addTrigger(self, user_id, command, stock_sym, amount, funds, timeadded):
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
        )
        Returning *;
        """.format(user_id, command, stock_sym, amount, funds, timeadded))

        result = self.cur.fetchone()

        #print('good')

        return result

    # Input: (user_id, command, stock_sym)
    # Output: The record that is deleted with highest timeadded (most recent)
    # Delete all records with user_id, command, stock_sym
    def removeTrigger(self, user_id, command, stock_sym):
        self.cur.execute("""
        Delete
        From Pending
        Where ctid --implicit line id
        In (
        Select ctid
        From Pending
        Where user_id = '{}' and command = '{}' and stock_sym = '{}'
        Order By timeadded desc
        )
        Returning *;
        """.format(user_id, command, stock_sym))

        result = self.cur.fetchone()

        #print(result)

        return result


    ##
    ## Audit
    ##

    # Input: (user_id, command, timeadded, [stock_sym, amount, funds, and cryptokey])
    # Output: The record that is created
    # Inserts a new record with (user_id, command, [stock_sym, amount, funds, and timeadded])
    # Puts Null if not given
    def addAudit(self, user_id, command, timeadded, stock_sym = None, amount = None, funds = None, cryptokey = None):
        self.cur.execute("""
        INSERT INTO Audit
        Values
        (
          Default, --incrementing id
          '{}',     --user_id
          '{}',     --command
          {},       --timeadded
          {},       --stock_sym
          {},       --amount
          {},       --funds
          {}        --cryptokey
        )
        Returning *;
        """.format
        (
            user_id,
            command,
            timeadded,
            ("'" + stock_sym + "'") if stock_sym else 'Null',
            amount if amount else 'Null',
            funds if funds else 'Null',
            ("'" + cryptokey + "'") if cryptokey else 'Null')
        )
        # The format looks weird to accommodate None -> Null

        result = self.cur.fetchone()

        #print('good')

        return result


    # Input: ([user_id])
    # Output: A list of all records [containing user_id]
    # If no records exist returns an empty list
    def dumpAudit(self, user_id = None):
        if user_id:
            self.cur.execute("""
            Select *
            From Audit
            Where user_id = '{}'
            Order By audit_id;
            """.format(user_id))
        else:
            self.cur.execute("""
            Select *
            From Audit
            Order By audit_id;
            """)

        result = self.cur.fetchall()

        #print(result)

        return result
