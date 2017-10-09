# coding=utf-8
"""
This is for controlling proxy ip
"""

import random
import time
from datetime import datetime, timedelta
import urllib2
import threading
import threadpool

from multiprocessing import Process
from sqlite_controller import SqliteController
from proxy_ip import ProxyIP, ProxyIPSet
from proxy_spider import ProxySpider

instance_lock = threading.Lock()


class ProxyController(object):
    """
    This is a class for crawling proxy ip
    """
    __instance = None

    __check_http_url = 'http://silvercodingcat.com/python/2017/08/09/Proxy-Spider-Check/'
    __check_https_url = ''
    __check_retry_time = 3
    __check_fake_proxy = True
    __thread_timeout = 15
    __thread_list_split = 3
    __thread_result = threading.local()

    __watcher_thread_stop = False
    __crawl_thread_running = False
    __crawl_check_seconds = 30
    __crawl_pool_max = 20

    __verify_thread_running = False
    __verify_check_seconds = 300
    __verify_proxy_minutes = 5
    __verify_pool_max = 30

    __proxy_spider = ProxySpider()
    __proxy_spider_page = 2

    __sql_create_table = "create table proxy_ip(id INTEGER primary key autoincrement, ip VARCHAR(20), port VARCHAR(10),https TINYINT,available TINYINT,verify_time TIMESTAMP default (datetime('now', 'localtime')), create_time TIMESTAMP default (datetime('now', 'localtime')))"
    __sql_insert = "insert into proxy_ip values(null, ?, ?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))"
    __sql_delete = 'delete from proxy_ip where id = ?'
    __sql_update = 'update proxy_ip set ip = ?, port = ?, https = ?, available = ?, verify_time = ? where id = ?'
    __sql_select_exist = 'select * from proxy_ip where ip = ? and port = ?'
    __sql_select_all = 'select * from proxy_ip'
    __sql_select_verify = 'select * from proxy_ip where verify_time < datetime(?) and available = 1'
    __sql_select_available_all = 'select * from proxy_ip where verify_time > datetime(?) and available = 1 order by verify_time desc'
    __sql_select_available_limit = 'select * from proxy_ip where verify_time > datetime(?) and available = 1 order by verify_time desc limit ? offset ?'
    __sql_select_available_count = 'select count(*) from proxy_ip where available = 1'

    __db_path = 'proxy_ip.db'
    __db_controller = SqliteController(__sql_create_table, __db_path)
    __db_min_storage = 20
    __db_min_available = 10

    def __init__(self):
        self.__db_controller.init_db()
        # check_process = Process(target=self.check_db_storage_thread, args=(
        #     self.check_db_storage_thread,))
        check_process = Process(target=self.check_db_storage_thread)
        check_process.start()
        verify_process = Process(target=self.verify_db_storage_thread)
        verify_process.start()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                instance_lock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(ProxyController, cls).__new__(
                        cls, *args, **kwargs)
            finally:
                instance_lock.release()
        return cls.__instance

    def send_check_request(self, opener, url):
        """
        Send request to check server
        """
        response = opener.open(url, timeout=self.__thread_timeout)
        return response.code == 200 and response.url == url

    def check_proxy(self, proxy_ip):
        """
        Check proxy available. Timeout: 15s. Retry: 3 times.
        """
        transfer_method = 'https' if proxy_ip.is_https else 'http'
        ip_port = proxy_ip.ip + ':' + proxy_ip.port
        proxy_data = {transfer_method: ip_port}
        check_url = self.__check_https_url if proxy_ip.is_https else self.__check_http_url
        proxy_handler = urllib2.ProxyHandler(proxy_data)
        opener = urllib2.build_opener(proxy_handler)
        result = False
        for i in range(self.__check_retry_time):
            try:
                result = self.send_check_request(opener, check_url)
                break
            except BaseException:
                continue
        proxy_ip.available = result
        return result

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
        print len(proxy_ip_list)
        times = len(proxy_ip_list) // split_num
        proxy_ip_split_list = []
        for i in range(times + 1):
            pre = i * split_num
            last = (i + 1) * split_num if i < times else len(proxy_ip_list)
            proxy_ip_split_list.append(proxy_ip_list[pre:last])
        pool = threadpool.ThreadPool(self.__crawl_pool_max)
        requests = threadpool.makeRequests(
            self.add_proxy_list_thread, proxy_ip_split_list)
        [pool.putRequest(request) for request in requests]
        pool.wait()
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
        self.insert_proxy_list_db(insert_list, False)

    def get_proxy(self, count=10, is_main_thread=True):
        """
        Get proxy list from splite and check available
        """
        ip_value_list = self.select_proxy_db(count, is_main_thread)
        ip_list = self.convert_db_proxy_to_proxy_ip(ip_value_list)
        random.shuffle(ip_list)
        return ProxyIPSet(ip_list)

    def insert_proxy_db(self, proxy_ip, is_main_thread=True):
        """
        Insert proxy ip info to sqlite db file.
        """
        sql = self.__sql_insert
        params_list = (proxy_ip.ip, proxy_ip.port,
                       1 if proxy_ip.is_https else 0, 1 if proxy_ip.available else 0)
        return self.__db_controller.sql_write(sql, params_list, is_main_thread)

    def insert_proxy_list_db(self, proxy_ip_list, is_main_thread=True):
        """
        Insert proxy ip info to sqlite db file.
        """
        ip_params_list = []
        sql = self.__sql_insert
        for proxy_ip in proxy_ip_list:
            ip_params = (proxy_ip.ip, proxy_ip.port,
                         1 if proxy_ip.is_https else 0, 1 if proxy_ip.available else 0)
            ip_params_list.append(ip_params)
        return self.__db_controller.sql_write_list(sql, ip_params_list, is_main_thread)

    def delete_proxy_db(self, proxy_ip, is_main_thread=True):
        """
        Delete proxy ip info from sqlite db file.
        """
        sql = self.__sql_delete
        params_list = []
        params_list.append(proxy_ip.db_id)
        return self.__db_controller.sql_write(sql, params_list, is_main_thread)

    def update_proxy_db(self, proxy_ip, is_main_thread=True):
        """
        Update proxy ip info in sqlite db file.
        """
        sql = self.__sql_update
        params_list = (proxy_ip.ip, proxy_ip.port, 1 if proxy_ip.is_https else 0,
                       1 if proxy_ip.available else 0, proxy_ip.verify_time, proxy_ip.db_id)
        return self.__db_controller.sql_write(sql, params_list, is_main_thread)

    def convert_db_proxy_to_proxy_ip(self, ip_value_list):
        """
        Convert data from db to proxy_ip instance
        """
        ip_list = []
        for ip_value in ip_value_list:
            ip_temp = ProxyIP(ip_value[1], ip_value[2],
                              ip_value[3] == 1, ip_value[4] == 1, ip_value[5], ip_value[6], ip_value[0])
            ip_list.append(ip_temp)
        return ip_list

    def select_proxy_db(self, count=None, is_main_thread=True):
        """
        Select proxy ip in sqlite
        """
        # result_set = self.__sqlite_controller.sql_read(self.__sql_select_ip_all, params_list)
        delta = timedelta(minutes=self.__verify_proxy_minutes)
        available_time = datetime.now() - delta
        str_available_time = available_time.strftime('%Y-%m-%d %H:%M:%S')
        if count is None:
            sql = self.__sql_select_available_all
            params_list = (str_available_time,)
        else:
            sql = self.__sql_select_available_limit
            params_list = (str_available_time, count, 0,)
        result_set = self.__db_controller.sql_read(
            sql, params_list, is_main_thread)
        if (not result_set or len(result_set) < self.__db_min_available) and not self.__crawl_thread_running:
            crawl_thread = threading.Thread(target=self.crawl_proxy_ip)
            crawl_thread.setName('proxy-spider')
            print 'Crawl proxy start'
            crawl_thread.start()
        proxy_ip_list = []
        for result in result_set:
            proxy_ip = result
            proxy_ip_list.append(proxy_ip)
        return proxy_ip_list

    def get_db_count(self, is_main_thread=True):
        """
        Get total record in db.
        """
        result_set = self.__db_controller.sql_read(
            self.__sql_select_available_count, None, is_main_thread)
        if result_set is not None and len(result_set) > 0 and len(result_set[0]) > 0:
            return result_set[0][0]
        else:
            return -1

    def check_db_storage_thread(self):
        """
        Check db storage status
        """
        time.sleep(3)
        crawl_thread = None
        while True:
            if self.__watcher_thread_stop:
                if crawl_thread is not None:
                    crawl_thread.join()
                break
            if not self.__crawl_thread_running:
                count = self.get_db_count(False)
                if count < self.__db_min_storage:
                    if not self.__crawl_thread_running:
                        crawl_thread = threading.Thread(
                            target=self.crawl_proxy_ip)
                        print 'Crawl proxy start'
                        crawl_thread.setName('crawl-spider')
                        crawl_thread.start()
            time.sleep(self.__crawl_check_seconds)

    def check_proxy_exist(self, proxy_ip):
        """
        Check proxy existed in sqlite
        """
        params_list = (proxy_ip.ip, proxy_ip.port,)
        result_set = self.__db_controller.sql_read(
            self.__sql_select_exist, params_list, False)
        return result_set is not None and len(result_set) > 0

    def crawl_proxy_ip(self):
        """
        Run the proxy spider to crawl new proxy ip
        """
        self.__crawl_thread_running = True
        try:
            proxy_ip_list = self.__proxy_spider.get_proxy_ip(
                False, self.__proxy_spider_page)
            self.add_proxy_list(proxy_ip_list)
        finally:
            self.__crawl_thread_running = False

    def select_need_check_proxy_list(self, is_main_thread=True):
        """
        Select proxy ip in sqlite
        """
        delta = timedelta(minutes=self.__verify_proxy_minutes)
        verify_time = datetime.now() - delta
        str_verify_time = verify_time.strftime('%Y-%m-%d %H:%M:%S')
        params_list = []
        params_list.append(str_verify_time)
        result_set = self.__db_controller.sql_read(
            self.__sql_select_verify, params_list, is_main_thread)
        if result_set is None:
            result_set = []
        proxy_ip_list = []
        for result in result_set:
            proxy_ip = result
            proxy_ip_list.append(proxy_ip)
        return proxy_ip_list

    def verify_db_storage_thread(self):
        """
        Check proxy in db is still available
        """
        verify_thread = None
        while True:
            if self.__watcher_thread_stop:
                if verify_thread is not None:
                    verify_thread.join()
                break
            if not self.__verify_thread_running:
                self.verify_proxy()
            time.sleep(self.__verify_check_seconds)

    def verify_proxy(self):
        """
        Check single proxy ip and delete inavaildable ip.
        """
        self.__verify_thread_running = True
        print 'verify proxy start'
        try:
            ip_value_list = self.select_need_check_proxy_list(False)
            proxy_ip_list = self.convert_db_proxy_to_proxy_ip(ip_value_list)
            self.verify_proxy_ip_list(proxy_ip_list)
        except StandardError, error:
            print error.message
        finally:
            self.__verify_thread_running = False
            print 'verify proxy done'

    def verify_proxy_ip_list(self, proxy_ip_list):
        """
        Check proxy ip list.
        """
        pool = threadpool.ThreadPool(self.__verify_pool_max)
        requests = threadpool.makeRequests(
            self.verify_proxy_ip_thread, proxy_ip_list)
        [pool.putRequest(request) for request in requests]
        pool.wait()

    def verify_proxy_ip_thread(self, proxy_ip):
        """
        Check single proxy ip and delete inavaildable ip.
        """
        if self.check_proxy(proxy_ip):
            proxy_ip.verify_time = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.update_proxy_db(proxy_ip, False)
        else:
            self.delete_proxy_db(proxy_ip, False)

    def add_black_list(self, proxy_ip, is_main_thread=True):
        """
        Add fake ip to sqlite. To not get any more
        """
        proxy_ip.available = 0
        self.update_proxy_db(proxy_ip, is_main_thread)

    def dispose(self):
        """
        Release resource.
        """
        self.__watcher_thread_stop = True
        self.__db_controller.dispose_db_connection()


if __name__ == '__main__':
    controller = ProxyController()
# controller2 = ProxyController()
# print id(controller)
# print id(controller2)
# ip_set = controller.get_proxy()
    while True:
        time.sleep(30)
# ip_list = controller.get_proxy()
# for ip in ip_list:
#     print ip.ip + '\t' + ip.port
