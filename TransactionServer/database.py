import psycopg2
import psycopg2.pool
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from contextlib import contextmanager

dbpool = None

def setUp():
    # Connecting to generic user
    conn = psycopg2.connect("dbname=postgres host=localhost user=postgres password=postgres")
    cur = conn.cursor()
    file = open("DBInit.sql", "r")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    # Set Database and user
    for line in file:
        print(line)
        cur.execute(line)
    file.close()
    cur.close()
    conn.commit()
    conn.close()

    global dbpool
    dbpool = psycopg2.pool.ThreadedConnectionPool(1,10,host="localhost",
                                                    dbname="daytrading",
                                                    user="seng468",
                                                    password="seng468",
                                                    )
    # Connecting to seng468 user
    file = open("daytrading.sql", "r")
    # Set up tables
    with db_cursor() as cur:
        cur.execute(file.read())
    file.close()

@contextmanager
def db_cursor():
    conn = dbpool.getconn()
    try:
        with conn.cursor() as cur:
            yield cur
            conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        dbpool.putconn(conn)

            #with dbcursor() as cur:
            # cur.execute()

class Database:

    def start(self):
        setUp()


    ##
    ## Users Table
    ##

    # Input: (user_id)
    # Output: (user_id, funds)
    # If no record is found returns None
    def selectUsers(self, user_id):
        result = ""
        with db_cursor() as cur:
            cur.execute("""
	           Select *
	           From users
	           Where user_id = '{}';
	           """.format(user_id))
            result = cur.fetchone()

        #print(result)
        return result

    # Input: (user_id, funds)
    # Output: The record that is created/updated
    # The record containing user_id has it's funds changed to input funds
    # If no record is found creates a record with user_id and funds
    def changeUsers(self, user_id, funds):
        result = ""
        with db_cursor() as cur:
            cur.execute("""
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
            result = cur.fetchone()

        #print('good')
        return result


    ##
    ## Accounts Table
    ##

    # Input: (user_id, stock_sym)
    # Output: (user_id, stock_sym, amount)
    # If no record is found returns None
    def selectAccount(self, user_id, stock_sym):
        with db_cursor() as cur:
            cur.execute("""
	           Select *
    	       From account
	           Where user_id = '{}' and stock_sym = '{}';
    	       """.format(user_id, stock_sym))

            result = cur.fetchone()

        #print(result)
        return result

    # Input: (user_id, stock_sym, amount)
    # Output: The record that is created/updated
    # The record containing user_id and stock_sym has it's amount changed to input amount
    # If no record is found creates a record with user_id, stock_sym and amount
    def changeAccount(self, user_id, stock_sym, amount):
        with db_cursor() as cur:
            cur.execute("""
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

            result = cur.fetchone()

        #print('good')
        return result


    ##
    ## Pending Table
    ##

    # Input: (user_id, command)
    # Output: (user_id, command, stock_sym, amount, funds, timeadded) with highest timeadded (most recent)
    # If no record is found returns None
    def selectPending(self, user_id, command):
        with db_cursor() as cur:
            cur.execute("""
	           Select *
	           From pending
	           Where user_id = '{}' and command = '{}'
	           Order By timeadded desc
	           limit 1;
	           """.format(user_id, command))

            result = cur.fetchone()

        #print(result)
        return result

    # Input: (user_id, command, stock_sym, amount, funds, timeadded)
    # Output: The record that is created
    # Inserts a new record with user_id, command, stock_sym, amount, funds, and timeadded
    def addPending(self, user_id, command, stock_sym, amount, funds, timeadded):
        with db_cursor() as cur:
            cur.execute("""
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

            result = cur.fetchone()

        #print('good')
        return result

    # Input: (user_id, command)
    # Output: The record that is deleted
    # Delete the record with user_id, command with highest timeadded (most recent)
    def removePending(self, user_id, command):
        with db_cursor() as cur:
            cur.execute("""
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

            result = cur.fetchone()

        #print(result)
        return result


    ##
    ## Triggers
    ##

    ##
    ## BuyTriggers
    ##

    # Input: (user_id, stock_sym)
    # Output: (user_id, stock_sym, reserve, trigger_amount)
    # If no record is found returns None
    def selectTrigger(self, user_id, command, stock_sym):
        with db_cursor() as cur:
            if command == 'SET_BUY_AMOUNT' or command == 'SET_BUY_TRIGGER':
                cur.execute("""
	               Select *
	               From BuyTriggers
	               Where user_id = '{}' and stock_sym = '{}'
	               """.format(user_id, stock_sym))

            else:
                cur.execute("""
	               Select *
	               From SellTriggers
	               Where user_id = '{}' and stock_sym = '{}'
	               """.format(user_id, stock_sym))

            result = cur.fetchone()

        #print(result)
        return result

    # Input: NONE
    # Output: A list of all completed triggers
    # If no record is found returns an empty list
    def selectAllTrigger(self):
        with db_cursor() as cur:
            cur.execute("""
	           Select *
	           From BuyTriggers
	           Where trigger_amount > 0
	           """)

            buyResult = cur.fetchall()

            cur.execute("""
	           Select *
	           From SellTriggers
	           Where trigger_amount > 0
	           """)

            sellResult = cur.fetchall()


        return buyResult + sellResult


    # Input: (user_id, stock_sym, reserve, trigger_amount)
    # Output: The record that is created/updated
    # The record containing user_id and stock_sym has it's reserve and trigger_amount changed to inputs
    # If no record is found creates a record with (user_id, stock_sym, reserve, trigger_amount)
    def changeTrigger(self, user_id, command, stock_sym, reserve, trigger_amount, amount=0):
        with db_cursor() as cur:
            if command == 'SET_BUY_AMOUNT' or command == 'SET_BUY_TRIGGER':
                cur.execute("""
                    INSERT INTO BuyTriggers
                    Values
                    (
                    '{0}', --user_id
                    '{1}', --stock_sym
                    {2},   --reserve
                    {3}    --trigger_amount
                    )
                    On Conflict (user_id, stock_sym)
                    DO
                    Update
                    SET reserve = {2}, trigger_amount = {3}
                    Returning *;
                    """.format(user_id, stock_sym, reserve, trigger_amount))

                result = cur.fetchone()
            else:
                cur.execute("""
                    INSERT INTO SellTriggers
                    Values
                    (
                    '{0}', --user_id
                    '{1}', --stock_sym
                    {2},   --reserve
                    {3},   --amount
                    {4}    --trigger_amount
                    )
                    On Conflict (user_id, stock_sym)
                    DO
                    Update
                    SET reserve = {2}, amount = {3}, trigger_amount = {4}
                    Returning *;
                    """.format(user_id, stock_sym, amount, reserve, trigger_amount))

                result = cur.fetchone()

        #print('good')sss
        return result


    # Input: (user_id, stock_sym)
    # Output: One record that is deleted
    # Delete all records with (user_id, stock_sym)
    def removeTrigger(self, user_id, command, stock_sym):
        with db_cursor() as cur:
            if command == 'SET_BUY_AMOUNT' or command == 'SET_BUY_TRIGGER':
                cur.execute("""
                    Delete
                    From BuyTriggers
                    Where user_id = '{}' and stock_sym = '{}'
                    Returning *;
                    """.format(user_id, stock_sym))

            else:
                cur.execute("""
                    Delete
                    From SellTriggers
                    Where user_id = '{}' and stock_sym = '{}'
                    Returning *;
                    """.format(user_id, stock_sym))

            result = cur.fetchone()

        #print(result)
        return result


    ##
    ## SellTriggers
    ##

    # Input: (user_id, stock_sym)
    # Output: (user_id, stock_sym, amount, reserve, trigger_amount)
    # If no record is found returns None
#    def selectTrigger(self, user_id, stock_sym):
#        self.cur.execute("""
#	    Select *
#	    From SellTriggers
#	    Where user_id = '{}' and stock_sym = '{}'
#	    """.format(user_id, stock_sym))
#
#        result = self.cur.fetchone()

        #print(result)

#        return result

    # Input: (user_id, stock_sym, amount, reserve, trigger_amount)
    # Output: The record that is created/updated
    # The record containing user_id and stock_sym has it's amount, reserve and trigger_amount changed to inputs
    # If no record is found creates a record with (user_id, stock_sym, amount, reserve, trigger_amount)
#    def changeTrigger(self, user_id, stock_sym, amount, reserve, trigger_amount):
#        self.cur.execute("""
#        INSERT INTO SellTriggers
#        Values
#        (
#          '{0}', --user_id
#          '{1}', --stock_sym
#          {2},   --reserve
#          {3},   --amount
#          {4}    --trigger_amount
#        )
#        On Conflict (user_id, stock_sym)
#        DO
#        Update
#        SET reserve = {2} and amount = {3} and trigger_amount = {4}
#        Returning *;
#        """.format(user_id, stock_sym, amount, reserve, trigger_amount))

#        result = self.cur.fetchone()

        #print('good')

#        return result


    # Input: (user_id, stock_sym)
    # Output: One record that is deleted
    # Delete all records with (user_id, stock_sym)
#    def removeTrigger(self, user_id, command, stock_sym):
#        self.cur.execute("""
#        Delete
#        From SellTriggers
#        Where user_id = '{}' and stock_sym = '{}'
#        Returning *;
#        """.format(user_id, stock_sym))

#        result = self.cur.fetchone()

        #print(result)

#        return result


    ##
    ## Audit
    ##

    # Input: (user_id, command, timeadded, [stock_sym, amount, funds, and cryptokey])
    # Output: The record that is created
    # Inserts a new record with (user_id, command, [stock_sym, amount, funds, and timeadded])
    # Puts Null if not given
    def addAudit(self, user_id, timeadded, server, command = None, stock_sym = None, amount = None, funds = None, cryptokey = None, filename = None, stock_price = None, quote_time = None, action = None, error_msg = None, debug_msg = None):
        with db_cursor() as cur:
            cur.execute("""
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
                {},       --cryptokey
                {},       --server
                {},       --filename
                {},       --stock_price
                {},       --quote_time
                {},       --action
                {},       --error_msg
                {}       --debug_msg
                )
                Returning *;
                """.format
                    (
                    user_id,
                    command if command else 'Null',
                    timeadded,
                    ("'" + stock_sym + "'") if stock_sym else 'Null',
                    amount if amount else 'Null',
                    funds if funds else 'Null',
                    ("'" + cryptokey + "'") if cryptokey else 'Null',
                    ("'" + server + "'"),
                    ("'" + filename + "'") if filename else 'Null',
                    stock_price if stock_price else 'Null',
                    ("'" + quote_time + "'") if quote_time else 'Null',
                    ("'" + action + "'") if action else 'Null',
                    ("'" + error_msg + "'") if error_msg else 'Null',
                    ("'" + debug_msg + "'") if debug_msg else 'Null')
                    )
                    # The format looks weird to accommodate None -> Null

            result = cur.fetchone()

        #print('good')
        return result


    # Input: ([user_id])
    # Output: A list of all records [containing user_id]
    # If no records exist returns an empty list
    def dumpAudit(self, user_id = None):
        with db_cursor() as cur:
            if user_id:
                cur.execute("""
                    Select *
                    From Audit
                    Where user_id = '{}'
                    Order By audit_id;
                    """.format(user_id))
            else:
                cur.execute("""
                Select *
                From Audit
                Order By audit_id;
                """)

            result = cur.fetchall()

        #print(result)
        return result



    # Input: user_id
    # Output:   (user_id, funds),
    #           [(user_id, stock_sym, amount), ...],
    #           [(user_id, command, stock_sym, amount, funds, timeadded), ...], all transactions (dumplog)
    #           [(user_id, command, stock_sym, amount, funds, timeadded), ...]  triggers
    # If any don't exist will return NONE, [], [], []
    def displaySummary(self, user_id):
        with db_cursor() as cur:
            balance = self.selectUsers(user_id)

            cur.execute("""
	           Select *
    	       From account
	           Where user_id = '{}';
    	       """.format(user_id))
            stocks = cur.fetchall()

            transactionHistory = self.dumpAudit(user_id)

            cur.execute("""
	           Select *
	           From pending
	           Where user_id = '{}' and command in ('SET_BUY_AMOUNT', 'SET_BUY_TRIGGER', 'SET_SELL_AMOUNT', 'SET_SELL_TRIGGER')
	           Order By timeadded desc
	           """.format(user_id))
            triggers = cur.fetchall()


        return balance, stocks, transactionHistory, triggers
