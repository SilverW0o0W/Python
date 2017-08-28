"""
This is the file for proxy ip class
"""

from datetime import datetime


class ProxyIP(object):
    """
    This is the class for ip information.
    """

    def __init__(self, ip, port, is_https, available=False, verify_time=None, create_time=None, id=None):
        self.id = id
        self.ip = ip
        self.port = port
        self.is_https = is_https
        self.available = available
        self.verify_time = verify_time if verify_time is not None else datetime.now(
        ).strftime('%Y-%m-%d %H:%M:%S')
        self.create_time = create_time if create_time is not None else datetime.now(
        ).strftime('%Y-%m-%d %H:%M:%S')

    def get_ip_port(self):
        """
        Get ip:port string.
        """
        return self.ip + ':' + self.port
