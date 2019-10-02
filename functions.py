import config
import mysql
import mysql.connector
from mysql.connector import errorcode

# DB FUNCTIONS

def connect_to_db(db):
    cnx1 = mysql.connector.connect(
        host = config.host,
        user = config.user,
        passwd = config.password,
        database = db)
    cursor = cnx1.cursor()
    return cursor, cnx1

def create_database_helper(cursor, database):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(database))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

def create_database(cursor, cnx, db_name):
    try:
        cursor.execute("USE {}".format(db_name))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database_helper(cursor, db_name)
            print("Database {} created successfully.".format(db_name))
            cnx.database = db_name
        else:
            print(err)
            exit(1)


def insert_to_dir(list_of_four, cursor):
    stmt = """
    INSERT INTO top_directors 
    (id, name, url, sign)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(stmt, list_of_four)