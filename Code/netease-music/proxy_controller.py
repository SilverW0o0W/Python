# coding=utf-8
"""
This is for controlling proxy ip
"""

import time
import threading
import urllib2

import os
import sqlite3

from proxy_spider import ProxyIP
from proxy_spider import ProxySpider


class ProxyController(object):
    """
    This is a class for crawling proxy ip
    """
    __check_http_url = 'http://silvercodingcat.com/python/2017/08/09/Proxy-Spider-Check/'
    __check_https_url = ''
    __thread_timeout = 15
    __thread_list_split = 5
    __thread_result = threading.local()

    __proxy_spider = ProxySpider()
    __proxy_spider_page = 2

    __db_path = 'proxy_ip.db'
    __db_connection = None
    __db_min_storage = 10
    __db_thread_connection = threading.local()

    __sql_create_table = 'create table proxy_ip(id INTEGER primary key autoincrement, ip VARCHAR(20), port VARCHAR(10),https TINYINT,available TINYINT)'
    __sql_insert_ip = 'insert into proxy_ip values(null, ?, ?, ?, ?)'
    __sql_select_ip_exist = 'select * from proxy_ip where ip = ? and port = ?'
    __sql_select_ip_all = 'select * from proxy_ip'

    def __init__(self):
        self.init_db()

    def send_check_request(self, proxy_data, check_url):
        """
        Send check request. Timeout: 15s. Retry: 3 times.
        """
        for i in range(3):
            check_thread = threading.Thread(
                target=self.send_check_request_thread, args=(proxy_data, check_url,))
            print 'retry' + str(i)
            check_thread.start()
            check_thread.join(self.__thread_timeout)
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
        except urllib2.HTTPError, error:
            self.__thread_result = False
            print error
        except urllib2.URLError, error:
            self.__thread_result = False
            print error.message

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

    def add_proxy(self, proxy_ip):
        """
        Check proxy available and add into sqlite db.
        """
        if self.check_proxy(proxy_ip):
            if self.check_proxy_exist(proxy_ip):
                return False
            else:
                self.insert_proxy_db(proxy_ip)
                return True

    def add_proxy_list(self, proxy_ip_list):
        """
        Check proxy available and add into sqlite db.
        """
        split_num = self.__thread_list_split

        times = len(proxy_ip_list) // split_num
        proxy_ip_split_list = []
        for i in range(times + 1):
            pre = i * split_num
            last = (i + 1) * split_num if i < times else len(proxy_ip_list)
            proxy_ip_split_list.append(proxy_ip_list[pre:last])
        for list_thread in proxy_ip_split_list:
            add_thread = threading.Thread(
                target=self.add_proxy_list_thread, args=(list_thread,))
            add_thread.start()
            add_thread.join()
        print 'add proxy done'

    def add_proxy_list_thread(self, proxy_ip_list):
        """
        Muiti-Threading check proxy.
        """
        insert_list = []
        for proxy_ip in proxy_ip_list:
            if self.check_proxy(proxy_ip):
                if self.check_proxy_exist(proxy_ip):
                    continue
                else:
                    insert_list.append(proxy_ip)
        self.insert_proxy_list_db(insert_list)

    def get_proxy(self, count=10):
        """
        Get proxy list from splite and check available
        """
        ip_value_list = self.select_proxy_db()
        ip_list = []
        for ip_value in ip_value_list:
            ip_temp = ProxyIP(ip_value[1], ip_value[2],
                              ip_value[3] == 1, ip_value[4] == 1)
            ip_list.append(ip_temp)
        while True:
            time.sleep(100)
        return ip_list

    def insert_proxy_db(self, proxy_ip):
        """
        Insert proxy ip info to sqlite db file.
        """
        sql = self.__sql_insert_ip
        params_list = (proxy_ip.ip, proxy_ip.port,
                       1 if proxy_ip.is_https else 0, 1 if proxy_ip.available else 0)
        return self.sql_write(sql, params_list)

    def insert_proxy_list_db(self, proxy_ip_list):
        """
        Insert proxy ip info to sqlite db file.
        """
        ip_params_list = []
        for proxy_ip in proxy_ip_list:
            sql = self.__sql_insert_ip
            ip_params = (proxy_ip.ip, proxy_ip.port,
                         1 if proxy_ip.is_https else 0, 1 if proxy_ip.available else 0)
            ip_params_list.append(ip_params)
        return self.sql_write_list(sql, ip_params_list, False)

    def select_proxy_db(self, count=10):
        """
        Select proxy ip in sqlite
        """
        params_list = (count)
        # result_set = self.sql_read(self.__sql_select_ip_all, params_list)
        result_set = self.sql_read(self.__sql_select_ip_all)
        if result_set is None or len(result_set) < self.__db_min_storage:
            crawl_thread = threading.Thread(target=self.crawl_proxy_ip)
            print 'Crawl proxy start'
            crawl_thread.start()
        proxy_ip_list = []
        for result in result_set:
            proxy_ip = result
            proxy_ip_list.append(proxy_ip)
        return proxy_ip_list

    def check_proxy_exist(self, proxy_ip):
        """
        Check proxy existed in sqlite
        """
        params_list = (proxy_ip.ip, proxy_ip.port,)
        result_set = self.sql_read(
            self.__sql_select_ip_exist, params_list, False)
        return result_set is not None and len(result_set) > 0

    def init_db(self, is_main_thread=True):
        """
        Initialize sqlite db.
        """
        try:
            db_exist = self.establish_db_connection(is_main_thread)
            if not db_exist:
                # Create db table
                return self.sql_write(self.__sql_create_table)
            return True
        except sqlite3.DatabaseError:
            return False

    def establish_db_connection(self, is_main_thread=True):
        """
        Establish sqlite connection. If it don't exist, create the db file.
        Return: The file is existed before exstablish connection.
        """
        is_exist = os.path.exists(self.__db_path)
        if is_main_thread:
            self.__db_connection = sqlite3.connect(self.__db_path)
        else:
            self.__db_thread_connection = sqlite3.connect(self.__db_path)
        return is_exist

    def dispose_db_connection(self):
        """
        Close db connection
        """
        if self.__db_connection != None:
            self.__db_connection.close()
            self.__db_connection = None

    def sql_write(self, sql, params_list=None, is_main_thread=True):
        """
        Execute sqlite sql. For write.
        """
        cursor = None
        connect = None
        try:
            if is_main_thread:
                connect = self.__db_connection
            else:
                self.establish_db_connection(False)
                connect = self.__db_thread_connection
            cursor = connect.cursor()
            if params_list is None:
                result = cursor.execute(sql)
            else:
                result = cursor.execute(sql, params_list)
            connect.commit()
            return result
        except sqlite3.DatabaseError, db_error:
            print db_error.message
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if is_main_thread is False and connect is not None:
                connect.close()

    def sql_write_list(self, sql, params_list, is_main_thread=True):
        """
        Execute sqlite sql. For write.
        """
        connect = None
        cursor = None
        row_num = 0
        try:
            if is_main_thread:
                connect = self.__db_connection
            else:
                self.establish_db_connection(False)
                connect = self.__db_thread_connection
            cursor = connect.cursor()
            for params in params_list:
                try:
                    result = cursor.execute(sql, params)
                    row_num += result.rowcount
                except sqlite3.DatabaseError:
                    continue
            connect.commit()
            return row_num
        except sqlite3.DatabaseError, db_error:
            print db_error.message
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if is_main_thread is False and connect is not None:
                connect.close()

    def sql_read(self, sql, params_list=None, is_main_thread=True):
        """
        Execute sqlite sql. For read.
        """
        connect = None
        cursor = None
        try:
            if is_main_thread:
                connect = self.__db_connection
            else:
                self.establish_db_connection(False)
                connect = self.__db_thread_connection
            cursor = connect.cursor()
            if params_list is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params_list)
            result_set = cursor.fetchall()
            return result_set
        except sqlite3.DatabaseError, db_error:
            print db_error.message
            return None
        finally:
            if cursor is not None:
                cursor.close()
            if is_main_thread is False and connect is not None:
                connect.close()

    def crawl_proxy_ip(self):
        """
        Run the proxy spider to crawl new proxy ip
        """
        proxy_ip_list = self.__proxy_spider.get_proxy_ip(
            self.__proxy_spider_page)
        add_proxy_ip_list = []
        for proxy_ip in proxy_ip_list:
            if proxy_ip.is_https == False:
                add_proxy_ip_list.append(proxy_ip)
        self.add_proxy_list(add_proxy_ip_list)


controller = ProxyController()
# proxy = ProxyIP('182.138.249.117', '8118', False, False)
# print controller.add_proxy(proxy)
ip_list = controller.get_proxy()
for ip in ip_list:
    print ip.ip + '\t' + ip.port
