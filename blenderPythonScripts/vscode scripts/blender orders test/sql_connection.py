# sql_connection.py
import pyodbc
from config import DB_SERVER, DB_DATABASE, DB_USERNAME, DB_PASSWORD

def connect_to_database():
    conn_str = f'DRIVER={{SQL Server}};SERVER={DB_SERVER};DATABASE={DB_DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD}'
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    return conn, cursor

def close_database_connection(conn):
    conn.close()

def retrieve_data(cursor):
    cursor.execute('SELECT * FROM "mesh-categorization"')
    return cursor.fetchall()
