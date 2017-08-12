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
    __sql_create_table = 'create table proxy_ip(id INT primary key autoincrement, ip VARCHAR(20), port VARCHAR(10),https TINYINT,available TINYINT)'
    __sql_insert_ip = 'insert into proxy_ip values(?, ?, ?, ?)'
    __sql_select_ip_exist = 'select * from proxy_ip where ip = ? and port = ?'

    def __init__(self):
        self.init_db()

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

    def check_proxy(self, proxy_ip):
        """
        Check proxy available
        """
        transfer_method = 'https' if proxy_ip.is_https else 'http'
        ip_port = proxy_ip.ip + ':' + proxy_ip.port
        proxy_data = {transfer_method: ip_port}
        check_url = self.__check_https_url if proxy_ip.is_https else self.__check_http_url
        proxy_ip.available = self.send_check_request(proxy_data, check_url)
        return proxy_ip.available

    def insert_proxy_db(self, proxy_ip):
        """
        Insert proxy ip info to sqlite db file.
        """
        sql = self.__sql_insert_ip
        params_list = (proxy_ip.ip, proxy_ip.port,
                       1 if proxy_ip.is_https else 0, 1 if proxy_ip.available else 0)
        return self.sql_execute(sql, params_list)

    def add_proxy(self, proxy_ip):
        """
        Check proxy available and add into sqlite db.
        """
        if self.check_proxy(proxy_ip):
            if self.check_proxy_exist(proxy_ip):
                return
            else:
                self.insert_proxy_db(proxy_ip)

    def check_proxy_exist(self, proxy_ip):
        """
        Check proxy existed in sqlite
        """
        params_list = (proxy_ip.ip, proxy_ip.port)
        result_set = self.sql_execute(self.__sql_select_ip_exist, params_list)
        return result_set != None and len(result_set) > 0

    def init_db(self):
        """
        Initialize sqlite db.
        """
        try:
            db_exist = self.establish_db_connection()
            if not db_exist:
                # Create db table
                return self.sql_execute(self.__sql_create_table)
            return True
        except sqlite3.DatabaseError:
            return False

    def establish_db_connection(self):
        """
        Establish sqlite connection. If it don't exist, create the db file.
        Return: The file is existed before exstablish connection.
        """
        is_exist = os.path.exists(self.__db_path)
        self.__db_conn = sqlite3.connect(self.__db_path)
        return is_exist

    def dispose_db_connection(self):
        """
        Close db connection
        """
        if self.__db_conn != None:
            self.__db_conn.close()
            self.__db_conn = None

    def sql_execute(self, sql, params_list=None):
        """
        Execute sqlite sql.
        """
        cursor = None
        try:
            cursor = self.__db_conn.cursor()
            if params_list is None:
                return cursor.execute(sql)
            else:
                return cursor.execute(sql, params_list)
        except sqlite3.DatabaseError:
            return None
        finally:
            cursor.close()


class ProxyIP(object):
    """
    This is the class for ip information.
    """

    def __init__(self, ip, port, is_https, available=False):
        self.ip = ip
        self.port = port
        self.is_https = is_https
        self.available = available

    def get_ip_port(self):
        """
        Get ip:port string.
        """
        return self.ip + ':' + self.port


spider = ProxySpider()
proxy = ProxyIP('221.201.81.248', '80', False, False)
print spider.add_proxy(proxy)
