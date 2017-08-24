"""
This is the file for proxy ip class
"""

import time

class ProxyIP(object):
    """
    This is the class for ip information.
    """

    def __init__(self, ip, port, is_https, available=False, verify_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))):
        self.ip = ip
        self.port = port
        self.is_https = is_https
        self.available = available
        self.verify_time = verify_time

    def get_ip_port(self):
        """
        Get ip:port string.
        """
        return self.ip + ':' + self.port
