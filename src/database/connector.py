import mysql.connector

db_config = {
    'host': '169.254.123.97',
    'port': 3307,
    'user': 'root',
    'password': '123456',
    'database': 'snpfinder'
}

def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection