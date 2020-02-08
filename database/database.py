import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class Database:

    def __init__(self):
        self.conn = psycopg2.connect("dbname=postgres host=localhost user=postgres password=postgres")
        self.cur = self.conn.cursor()
        file = open("DBInit.sql", "r")
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        for line in file:
            print(line)
            self.cur.execute(line)
        file.close()
        self.cur.close()
        self.conn.close()
        self.conn = psycopg2.connect("dbname=daytrading user=seng468 password='seng468'")
        self.cur = self.conn.cursor()
        file = open("daytrading.sql", "r")
        self.cur.execute(file.read())
        file.close()
        

    def close(self):
        self.cur.close()        
        self.conn.close()


    def selectUsers(self, user_id):
        self.cur.execute("""
	    Select *
	    From users
	    Where user_id = '{}';   
	    """.format(user_id))

        result = self.cur.fetchone()

        #print(result)

        return result

    def selectAccount(self, user_id, stock_sym):
        self.cur.execute("""
	    Select *
    	From account
	    Where user_id = '{}' and stock_sym = '{}';   
    	""".format(user_id, stock_sym))

        result = self.cur.fetchone()
	
        #print(result)

        return result

    def selectPending(self, user_id, command):
        self.cur.execute("""
	    Select *
	    From pending
	    Where user_id = '{}' and command = '{}'
	    Order By timeadded
	    limit 1;   
	    """.format(user_id, command))

        result = self.cur.fetchone()
    
        #print(result)

        return result 


    def changeUsers(self, user_id, funds):
        self.cur.execute("""
        INSERT INTO Users
        Values
        (
          '{}',
          {}
        )
        On Conflict (user_id)
        DO
        Update
        SET funds = {};
        """.format(user_id, funds, funds))

        #result =self.cur.fetchone()
    
        #print('good')

        return 'good' 



