import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def createDB():
    file = open("DBInit.sql", "r")    
    conn = None
    
    try:
        print('Creating a database...')
        conn = psycopg2.connect("dbname=postgres user=postgres password=postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        for line in file:
            print(line)
            cur.execute(line) 
        cur.close()
        file.close()
    #need to close some open readers
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
	
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def addTables():
    file = open("daytrading.sql", "r")
    conn = None
    
    try:
        print('Adding tables...')
        conn = psycopg2.connect("dbname=daytradedb user=seng468tracker password=SENG$^*")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        cur.execute(file.read())
		
        cur.close()
        file.close()
    #need to close some open readers
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
			
def changeFund(user, funds):
    return None
	
def changeFund(user, stock, sock_price):
    return None



def connect():
    createDB()
    addTables()

    

    f = open("log.txt", "w")
	
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
 
        # connect to the PostgreSQL server
        print('Connecting to daytradedb database...')
        conn = psycopg2.connect("dbname=daytradedb user=seng468tracker password=SENG$^*")
      
        # create a cursor
        cur = conn.cursor()
        
        
        #execute audit trail
        cur.execute('SELECT * FROM audittrail;')
		
        # display the PostgreSQL database server version
        audit_table = cur.fetchall()
        for s in audit_table:
            f.write(','.join(str(v) for v in s))
       
        # close the communication with the PostgreSQL
        cur.close()
        # close files
        f.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
 
if __name__ == '__main__':
    connect()