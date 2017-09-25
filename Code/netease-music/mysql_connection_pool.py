"""
This file work for controlling mysql connection pool.
"""

import threading
from mysql_controller import MysqlController

connection_lock = threading.Lock()


class ConnectionPool(object):
    """
    For control mysql connection.
    """

    _dispose = False

    def __init__(self, user, password, database, host='127.0.0.1', port=3306, max_connection=5, expire_time=30):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.max_connection = max_connection
        self.expire_time = expire_time
        self.list_active = []
        self.list_busy = []

    def check_connection_thread(self):
        pass

    def create_connection(self):
        controller = MysqlController(
            self.user, self.password, self.database, self.host, self.port)
