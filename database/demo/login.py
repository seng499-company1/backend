"""
Simple login demo to demonstrate loging into the database from Python.
"""

import mysql.connector

DB_CONN = mysql.connector.connect(user='api_user',
                                  password='password',
                                  host='127.0.0.1',
                                  database='scheduler')

CURSOR = DB_CONN.cursor()

CURSOR.execute("SHOW TABLES;")

DB_CONN.close()
