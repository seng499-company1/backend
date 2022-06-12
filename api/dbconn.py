"""
This file holds a lobal variable which allows the API to maintain a consitent connection to the
mysql database and the class that allows that.
"""
import mysql.connector

class DBConn:
    """This class maintains a consistent connection to the mysql database. Creating the db
    connection when a user first tries to get the connection instead of when the object is created
    allows the database time to fully start up before a connection is established.
    """

    def __init__(self):
        self.conn = None

    @staticmethod
    def connection():
        """Creates a database connection and returns it."""
        return mysql.connector.connect(user='api_user',
                                       password='password',
                                       host='127.0.0.1',
                                       database='scheduler')

    def get_conn(self):
        """Returns the database connection if it exists, else create it then return it."""
        if self.conn is None:
            self.conn = DBConn.connection()

        return self.conn

    def insert(self, sql):
        """Takes an sql insert statement to run and performs the neccessary calls to run it."""
        conn = self.get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def select(self, sql):
        """Takes an sql select statement to run and performs the neccessary calls to run it.
        Returns a dictionary of the results."""
        cursor = self.get_conn().cursor(dictionary=True)
        cursor.execute(sql)
        return cursor.fetchall()

DB_CONN = DBConn()
