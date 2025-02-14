import sys
import mysql.connector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from config import DATABASE_URL, DATABASE_PORT, DATABASE_USER, DATABASE_PASSWORD, DATABASE_SCHEMA

db_config = {
    'host': DATABASE_URL,
    'port': DATABASE_PORT,
    'user': DATABASE_USER,
    'password': DATABASE_PASSWORD,
    'database': DATABASE_SCHEMA
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection