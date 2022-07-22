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
            try:
                retval = mysql.connector.connect(**config)
            except: # pylint: disable=bare-except
                # This exception will be thrown if using a prod environment instead of docker
                # so this sets the host to JAWS DB which is used for prod.
                config['user'] = 'hdqz2q7qyb1bys07'
                config['password'] = 'jejgtg12efo5qw3p'
                config['host'] = 'wcwimj6zu5aaddlj.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
                config['database'] = 'fxk6nzr07ofh3rkm'
                retval = mysql.connector.connect(**config)
        except:
            # This exception will be thrown if using a local dev environment
            # so this sets the host to localhost which is used when not using docker. If an
            # expection is thrown again then something is actually wrong.
            config['host'] = '127.0.0.1'
            retval = mysql.connector.connect(**config)
        return retval

    def get_conn(self):
        """Returns the database connection if it exists, else create it then return it."""
        if self.conn is None or not self.conn.is_connected():
            self.conn = DBConn.connection()

        return self.conn

    def execute(self, sql):
        """
        Takes an sql insert or delete statement to run and performs the neccessary calls to run it.
        Returns true if item was inserted or deleted successfully, false otherwise.
        """
        conn = self.get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except mysql.connector.Error as errmsg:
            errmsg = f'Failed to execute query\
                        \n{sql}\
                        \nError: {errmsg}\n'
            conn.close()
            return errmsg

        conn.commit()

        if cursor.rowcount == 0:
            return "Failed to execute"

        conn.close()

        return True

    def multi_execute(self, sql_arr):
        """
        Takes an array of string sql queries to execute it in one automic function
        Returns true if all queries were sucessfully executed
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        for sql in sql_arr:
            try:
                cursor.execute(sql)
            except mysql.connector.Error as errmsg:
                errmsg = f'Failed to execute query\
                            \n{sql}\
                            \nError: {errmsg}\n'
                conn.close()
                return errmsg

        conn.commit()
        conn.close()

        return True

    def uuid(self):
        """Returns a uuid as a string generated by mysql."""
        conn = self.get_conn()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT UUID() AS uuid')
        uuid = cursor.fetchall()[0]['uuid']
        conn.close()

        return uuid

    def select_one(self, sql, bool_fields=None):
        """Takes an sql select statement to run and performs the neccessary calls to run it.
        Only returns one object compared to select which returns an array of objects.
        Returns a json object of the result. bool_fields are the fields which should be changed
        from sql's 1s and 0s to json true and false."""
        conn = self.get_conn()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(sql)
        except mysql.connector.Error as errmsg:
            errmsg = f'Failed to execute query\
                        \n{sql}\
                        \nError: {errmsg}\n'
            cursor.close()
            return errmsg

        result = cursor.fetchone()
        conn.close()

        #empty result
        if result is None:
            return None

        # changes all 1s and 0s returned by mysql to Python True and false
        if bool_fields:
            for field in bool_fields:
                result[field] = not result[field]

        return jsonify(result)

    def select(self, sql, bool_fields=None):
        """Takes an sql select statement to run and performs the neccessary calls to run it.
        Returns a json object of the results. bool_fields are the fields which should be changed
        from sql's 1s and 0s to json true and false."""
        conn = self.get_conn()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(sql)
        except mysql.connector.Error as errmsg:
            errmsg = f'Failed to execute query\
                        \n{sql}\
                        \nError: {errmsg}\n'
            cursor.close()
            return errmsg

        results = cursor.fetchall()
        conn.close()

        # changes all 1s and 0s returned by mysql to Python True and false
        if bool_fields:
            for i, result in enumerate(results):
                for field in bool_fields:
                    results[i][field] = bool(result[field])

        return jsonify(results)

DB_CONN = DBConn()
