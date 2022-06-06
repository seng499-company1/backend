import mysql.connector

conn = mysql.connector.connect(user='api_user',
	password='password', 
	host='127.0.0.1',
	database='scheduler')

conn.close()
