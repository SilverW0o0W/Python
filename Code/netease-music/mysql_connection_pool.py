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
        self.queue_available = Queue(max_connection)
        self.connection_busy = 0
        self.retry_time = 3
        self.pool_dispose = False

    def check_connection_thread(self):
        """
        Contorl connection number. Connect and dispose.
        """
        while True:
            if self.pool_dispose:
                break
            connection_lock.acquire()
            count = self.queue_available.qsize() + self.connection_busy
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
            self.append_connection(controller)

    def append_connection(self, controller):
        """
        Add connection to queue
        """
        connection_lock.acquire()
        if not self.pool_dispose:
            self.queue_available.put(controller)
        connection_lock.release()

    def get_connection(self):
        """
        Get connection.
        """
        connection = None
        for i in range(self.retry_time):
            connection_lock.acquire()
            try:
                if self.queue_available.qsize() > 0:
                    connection = self.queue_available.get()
                    break
                time.sleep(3)
            finally:
                connection_lock.release()
        if not connection:
            # need more detail
            raise Exception()
        return connection

    def close(self):
        """
        Close available connection.
        """
        self.pool_dispose = False
        connection_lock.acquire()
        try:
            break
        finally:
            connection_lock.release()


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
        if self.pool.pool_dispose:
            return False
        if self.reference_count >= self.pool.max_reference:
            return False
        if self.connect_time + self.pool.expire_delta < datetime.now():
            return False
        return True

    def close(self):
        """
        Close busy connection
        """
        if self.check_available():
            self.pool.append_connection(self)
        else:
            self.real_close()
        connection_lock.acquire()
        self.pool.connection_busy -= 1
        connection_lock.release()

    def real_close(self):
        """
        Close connection
        """
        super(PoolController, self).close()
