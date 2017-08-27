# coding=utf-8
"""
This is for controlling proxy ip
"""

import time
import threading
import urllib2

from sqlite_controller import SqliteController
from proxy_ip import ProxyIP
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

    __watcher_thread_stop = False
    __crawl_thread_running = False
    __crawl_check_seconds = 30
    __verify_thread_running = False
    __db_check_seconds = 300

    __proxy_spider = ProxySpider()
    __proxy_spider_page = 2

    __sql_create_table = "create table proxy_ip(id INTEGER primary key autoincrement, ip VARCHAR(20), port VARCHAR(10),https TINYINT,available TINYINT,verify_time TIMESTAMP default (datetime('now', 'localtime')), create_time TIMESTAMP default (datetime('now', 'localtime')))"
    __sql_insert_ip = "insert into proxy_ip values(null, ?, ?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))"
    __sql_delete_ip = 'delete from proxy_ip where id = ?'
    __sql_update_ip = 'update proxy_ip set ip = ?, port = ?, https = ?, available = ?, verify_time = ? where id = ?'
    __sql_select_ip_exist = 'select * from proxy_ip where ip = ? and port = ?'
    __sql_select_ip_all = 'select * from proxy_ip'
    __sql_select_ip_count = 'select count(*) from proxy_ip'

    __db_path = 'proxy_ip.db'
    __db_controller = SqliteController(__sql_create_table, __db_path)
    __db_min_storage = 10

    def __init__(self):
        self.__db_controller.init_db()
        check_thread = threading.Thread(target=self.check_db_storage_thread)
        check_thread.setName('storage_count_checker')
        check_thread.start()
        verify_thread = threading.Thread(target=self.verify_db_storage_thread)
        verify_thread.setName('storage_available_checker')
        verify_thread.start()

    def send_check_request(self, proxy_data, check_url):
        """
        Send check request. Timeout: 15s. Retry: 3 times.
        """
        for i in range(3):
            check_thread = threading.Thread(
                target=self.send_check_request_thread, args=(proxy_data, check_url,))
            # print 'retry' + str(i)
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
            # print error
        except urllib2.URLError, error:
            self.__thread_result = False
            # print error.message

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
        print len(proxy_ip_list)
        times = len(proxy_ip_list) // split_num
        proxy_ip_split_list = []
        for i in range(times + 1):
            pre = i * split_num
            last = (i + 1) * split_num if i < times else len(proxy_ip_list)
            proxy_ip_split_list.append(proxy_ip_list[pre:last])
        i = 0
        for list_thread in proxy_ip_split_list:
            add_thread = threading.Thread(
                target=self.add_proxy_list_thread, args=(list_thread,))
            add_thread.setName('add-proxy-' + str(i))
            add_thread.start()
            add_thread.join()
            i += 1
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

    def get_proxy(self, count=10):
        """
        Get proxy list from splite and check available
        """
        ip_value_list = self.select_proxy_db(count)
        return self.convert_db_proxy_to_proxy_ip(ip_value_list)

    def insert_proxy_db(self, proxy_ip, is_main_thread=True):
        """
        Insert proxy ip info to sqlite db file.
        """
        sql = self.__sql_insert_ip
        params_list = (proxy_ip.ip, proxy_ip.port,
                       1 if proxy_ip.is_https else 0, 1 if proxy_ip.available else 0)
        return self.__db_controller.sql_write(sql, params_list, is_main_thread)

    def insert_proxy_list_db(self, proxy_ip_list, is_main_thread=True):
        """
        Insert proxy ip info to sqlite db file.
        """
        ip_params_list = []
        for proxy_ip in proxy_ip_list:
            sql = self.__sql_insert_ip
            ip_params = (proxy_ip.ip, proxy_ip.port,
                         1 if proxy_ip.is_https else 0, 1 if proxy_ip.available else 0)
            ip_params_list.append(ip_params)
        return self.__db_controller.sql_write_list(sql, ip_params_list, is_main_thread)

    def delete_proxy_db(self, proxy_ip, is_main_thread=True):
        """
        Delete proxy ip info from sqlite db file.
        """
        sql = self.__sql_delete_ip
        params_list = []
        params_list.append(proxy_ip.id)
        return self.__db_controller.sql_write(sql, params_list, is_main_thread)

    def update_proxy_db(self, proxy_ip, is_main_thread=True):
        """
        Update proxy ip info in sqlite db file.
        """
        sql = self.__sql_update_ip
        params_list = (proxy_ip.ip, proxy_ip.port, 1 if proxy_ip.is_https else 0,
                       1 if proxy_ip.available else 0, proxy_ip.verify_time, proxy_ip.id)
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

    def select_proxy_db(self, count=10, is_main_thread=True):
        """
        Select proxy ip in sqlite
        """
        params_list = (count)
        # result_set = self.__sqlite_controller.sql_read(self.__sql_select_ip_all, params_list)
        result_set = self.__db_controller.sql_read(
            self.__sql_select_ip_all, is_main_thread)
        if (result_set is None or len(result_set) < self.__db_min_storage) and not self.__crawl_thread_running:
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
            self.__sql_select_ip_count, None, is_main_thread)
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
            self.__sql_select_ip_exist, params_list, False)
        return result_set is not None and len(result_set) > 0

    def crawl_proxy_ip(self):
        """
        Run the proxy spider to crawl new proxy ip
        """
        self.__crawl_thread_running = True
        try:
            proxy_ip_list = self.__proxy_spider.get_proxy_ip(
                self.__proxy_spider_page)
            add_proxy_ip_list = []
            for proxy_ip in proxy_ip_list:
                if not proxy_ip.is_https:
                    add_proxy_ip_list.append(proxy_ip)
            self.add_proxy_list(add_proxy_ip_list)
        finally:
            self.__crawl_thread_running = False

    def select_need_check_proxy_list(self, is_main_thread=True):
        """
        Select proxy ip in sqlite
        """
        result_set = self.__db_controller.sql_read(
            self.__sql_select_ip_all, None, is_main_thread)
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
        time.sleep(5)
        while True:
            if self.__watcher_thread_stop:
                if verify_thread is not None:
                    verify_thread.join()
                break
            if not self.__verify_thread_running:
                self.verify_proxy()
            time.sleep(self.__db_check_seconds)

    def verify_proxy(self):
        """
        Check single proxy ip and delete inavaildable ip.
        """
        self.__verify_thread_running = True
        ip_value_list = self.select_need_check_proxy_list(False)
        proxy_ip_list = self.convert_db_proxy_to_proxy_ip(ip_value_list)
        verify_thread = threading.Thread(
            target=self.verify_proxy_ip_list_thread, args=(proxy_ip_list,))
        verify_thread.start()
        verify_thread.join()
        self.__verify_thread_running = False

    def verify_proxy_ip_list_thread(self, proxy_ip_list):
        """
        Check proxy ip list.
        """
        check_thread_list = []
        for proxy_ip in proxy_ip_list:
            check_thread = threading.Thread(
                target=self.verify_proxy_ip_thread, args=(proxy_ip,))
            check_thread.start()
            check_thread_list.append(check_thread)
        for check_thread in check_thread_list:
            check_thread.join()

    def verify_proxy_ip_thread(self, proxy_ip):
        """
        Check single proxy ip and delete inavaildable ip.
        """
        available = self.check_proxy(proxy_ip)
        print 'verify' + proxy_ip.ip
        if available:
            proxy_ip.verify_time = time.strftime(
                '%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.update_proxy_db(proxy_ip, False)
        else:
            self.delete_proxy_db(proxy_ip, False)


controller = ProxyController()
# proxy = ProxyIP('182.138.249.117', '8118', False, False)
# print controller.add_proxy(proxy)
print controller.get_db_count()
while True:
    time.sleep(5)
# ip_list = controller.get_proxy()
# for ip in ip_list:
#     print ip.ip + '\t' + ip.port
