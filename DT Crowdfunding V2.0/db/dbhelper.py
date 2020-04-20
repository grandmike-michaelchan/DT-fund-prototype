import sqlite3

# DBMS location
DB_FILES = './db/database.db'


# create database table
def create_tables():
    # execute create table SQL statement from store-schema.sql
    f_name = 'db/store-schema.sql'
    with open(f_name, 'r', encoding='utf-8') as f:
        sql = f.read()
        # Establish database connection
        conn = sqlite3.connect(DB_FILES)
        try:
            # execute database script
            conn.executescript(sql)
            print('Database initialize success')
        except Exception as e:
            print('database initialize fail')
            print(e)
        finally:
            # close database connection
            conn.close()


# insert record into database
def load_data():
    # execute insert record SQL statement from store-dataload.sql
    f_name = './db/store-dataload.sql'
    with open(f_name, 'r', encoding='utf-8') as f:
        sql = f.read()
        # Establish database connection
        conn = sqlite3.connect(DB_FILES)
        try:
            # execute database script
            conn.executescript(sql)
            print('Data insertion success')
        except Exception as e:
            print('Data insertion fail')
            print(e)
        finally:
            # close database connection
            conn.close()
