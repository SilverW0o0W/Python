# coding=utf-8
"""
This is for proxy server, avoid to ban the own ip.
"""

import threading
import urllib2

import os
import sqlite3


class ProxySpider(object):
    """
    This is a class for crawling proxy ip
    """
    __check_http_url = 'http://silvercodingcat.com/python/2017/08/09/Proxy-Spider-Check/'
    __check_https_url = ''
    __thread_result = threading.local()

    __db_path = 'proxy_ip.db'
    __db_conn = None
    __db_sql_create_table = 'create table proxy_ip(id INT primary key, ip VARCHAR(20), port VARCHAR(10),method TINYINT,available TINYINT)'

    def send_check_request(self, proxy_data, check_url):
        """
        Send check request. Timeout: 10s. Retry: 3 times.
        """
        for i in range(3):
            check_thread = threading.Thread(
                target=self.send_check_request_thread, args=(proxy_data, check_url,))
            print 'retry' + str(i)
            check_thread.start()
            check_thread.join(10)
            if check_thread.is_alive():
                continue
            else:
                return self.__thread_result
        return False

    def send_check_request_thread(self, proxy_data, url):
        """
        Send request to check server
        """
        proxy_handler = urllib2.ProxyHandler(proxy_data)
        opener = urllib2.build_opener(proxy_handler)
        try:
            response = opener.open(url)
            self.__thread_result = response.code == 200
        except urllib2.URLError:
            self.__thread_result = False

    def check_proxy(self, is_https, ip_port):
        """
        Check proxy available
        """
        transfer_method = 'https' if is_https else 'http'
        proxy_data = {transfer_method: ip_port}
        check_url = self.__check_http_url if is_https else self.__check_https_url
        return self.send_check_request(proxy_data, check_url)

    def establish_db_onnection(self):
        """
        Establish sqlite connection. If it don't exist, create the db file.
        Return: The file is existed before exstablish connection.
        """
        is_exist = os.path.exists(self.__db_path)
        self.__db_conn = sqlite3.connect(self.__db_path)
        return is_exist

    def create_db_table(self, sql=__db_sql_create_table):
        """
        Create the proxy ip table.
        """
        cursor = self.__db_conn.cursor()
        cursor.execute(sql)
        cursor.close()


class ProxyIP(object):
    """
    This is the class for ip information.
    """

    def __init__(self, ip='', port='', is_https=False, available=False):
        self.__ip = ip
        self.__port = port
        self.__is_https = is_https
        self.__available = available


spider = ProxySpider()
print spider.check_proxy(False, '221.201.81.248:80')
