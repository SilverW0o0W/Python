# coding=utf-8
"""
For write comment detail to DB
"""

from music import CommentDetail
from multiprocessing import Process, Pipe


class CommentWriter(object):
    """
    For writing comment to DB
    """

    def __init__(self, flush_count=5):
        self.pipe = Pipe(duplex=False)
        self.flush_count = flush_count

    def send(self, data):
        """
        Send data to input process
        """
        if  isinstance(data,CommentDetail):
            pass