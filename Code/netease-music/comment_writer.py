# coding=utf-8
"""
For write comment detail to DB
"""

import threading
from multiprocessing import Process, Pipe
from music import CommentDetail

LOCK = threading.Lock()


class CommentWriter(object):
    """
    For writing comment to DB
    """

    def __init__(self, flush_count=5):
        self.pipe = Pipe(duplex=False)
        self.flush_count = flush_count
        self.is_run = True

    def _writing_process(self, pipe):
        buffer_message = []
        buffer_count = 0
        while True:
            message = pipe.recv()
            if not message:
                if buffer_count != 0:
                    pass
                break
            buffer_count += 1
            buffer_message.append(message)
            if buffer_count >= self.flush_count:
                pass
                buffer_message = []
                buffer_count = 0

    def send(self, data):
        """
        Send data to input process
        """
        if not self.is_run or not data:
            return
        LOCK.acquire()
        if self.is_run:
            self.pipe[1].send(data)
        LOCK.release()

    def dispose(self):
        """
        Close write process
        """
        LOCK.acquire()
        self.pipe[1].send(None)
        self.is_run = False
        LOCK.release()
