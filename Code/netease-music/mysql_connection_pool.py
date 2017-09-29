"""
This file work for controlling mysql connection pool.
"""

from Queue import Queue
from datetime import datetime, timedelta

import time
import threading
from mysql_controller import MysqlController

connection_lock = threading.Lock()


class ConnectionPool(object):
    """
    For control mysql connection.
    """

    def __init__(self, user, password, database, host='127.0.0.1', port=3306, max_connection=10):
        self.user = user
        self.password = password
        self.database = database
        self.host = host
        self.port = port
        self.max_connection = max_connection
        self.expire_time = 30
        self.expire_delta = timedelta(minutes=self.expire_time)
        self.max_reference = 10
        self.queue_active = Queue(max_connection)
        self.connection_busy = 0
        self.pool_dispose = False

    def check_connection_thread(self):
        """
        Contorl connection number. Connect and dispose.
        """
        while True:
            if self.pool_dispose:
                break
            connection_lock.acquire()
            count = self.queue_active.qsize() + self.connection_busy
            connection_lock.release()
            if count != self.max_connection:
                self.create_connection(self.max_connection - count)
            time.sleep(5)

    def create_connection(self, number=1):
        """
        Create new connection
        """
        for i in range(number):
            controller = PoolController(self)
            self.queue_active.put(controller)

    def get_connection(self):
        """
        Get connection.
        """
        # connection_lock.acquire(timeout = xxx)
        # code
        # connection_lock.release()

class PoolController(MysqlController):
    """
    The mysql controller for connection pool
    """

    def __init__(self, pool):
        self.pool = pool
        MysqlController.__init__(
            pool.user, pool.password, pool.database, pool.host, pool.port)
        self.reference_count = 0

    def connect(self):
        pass

    def check_available(self):
        """
        Chcek the instance connnection reference and expire
        """
        if self.reference_count >= self.pool.max_reference:
            return False
        if self.connect_time + self.pool.expire_delta < datetime.now():
            return False
        return True

    def close(self):
        if self.check_available():
            self.pool.queue_active.put(self)
        else:
            super(PoolController, self).close()
        connection_lock.acquire()
        self.pool.connection_busy -= 1
        connection_lock.release()
