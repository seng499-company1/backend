"""
This file holds a lobal variable which allows the API to maintain a consitent connection to the
mysql database and the class that allows that.
"""
import mysql.connector
from flask import jsonify

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
        config = {
            "user": 'api_user',
            "password": 'password',
            "host": 'db',
            "database": 'scheduler'
        }

        try:
            retval = mysql.connector.connect(**config)
        except mysql.connector.errors.DatabaseError:
            # This exception will be thrown if using a local dev environment instead of docker
            # so this sets the host to localhost which is used when not using docker. If an 
            # expection is thrown again then something is actually wrong.
            config['host'] = '127.0.0.1'
            retval = mysql.connector.connect(**config)

        return retval

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

    def select(self, sql, bool_fields=None):
        """Takes an sql select statement to run and performs the neccessary calls to run it.
        Returns a json object of the results. bool_fields are the fields which should be changed
        from sql's 1s and 0s to json true and false."""
        cursor = self.get_conn().cursor(dictionary=True)
        cursor.execute(sql)
        results = cursor.fetchall()

        # changes all 1s and 0s returned by mysql to Python True and false
        if bool_fields:
            for i, result in enumerate(results):
                for field in bool_fields:
                    results[i][field] = not result[field]

        return jsonify(results)

DB_CONN = DBConn()
