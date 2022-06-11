"""
Global variable which allows the API to maintain a consitent connection to the mysql database.
"""
import mysql.connector

# class DBConn:
#     def __init__(self):
#         self.db = self.connect()

#     # Returns a connection to the database
#     def connect(self):
#         return mysql.connector.connect(user='api_user',
#                                        password='password',
#                                        host='127.0.0.1',
#                                        database='scheduler')

DB_CONN = mysql.connector.connect(user='api_user',
                                  password='password',
                                  host='127.0.0.1',
                                  database='scheduler')
