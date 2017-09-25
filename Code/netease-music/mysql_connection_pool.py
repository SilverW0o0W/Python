"""
This file work for controlling mysql connection pool.
"""

import mysql_controller


class ConnectionPool(object):
    """
    For control mysql connection.
    """

    def __init__(self, user, password, database, host='127.0.0.1', port=3306, max_connection=5, expire_time=30):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.max_connection = max_connection
        self.expire_time = expire_time
