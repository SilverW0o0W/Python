# coding=utf-8
"""
This is for proxy server, avoid to ban the own ip.
"""

import threading
import urllib2

class ProxySpider(object):
    """
    This is a class for crawling proxy ip
    """
    __check_http_url = 'http://silvercodingcat.com/python/2017/08/09/Proxy-Spider-Check/'
    __check_https_url = ''
    __thread_result = threading.local()

    def send_check_request(self, proxy_data, check_url):
        """
        Send check request. Timeout: 10s. Retry: 3 times.
        """
        for i in range(3):
            check_thread = threading.Thread(target=self.send_check_request_thread, args=(proxy_data, check_url,))
            print 'retry'+ str(i)
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

    def check_proxy(self, is_http, ip_port):
        """
        Check proxy available
        """
        transfer_method = 'http' if is_http else 'https'
        proxy_data = {transfer_method: ip_port}
        check_url = self.__check_http_url if is_http else self.__check_https_url
        return self.send_check_request(proxy_data, check_url)

spider = ProxySpider()
print spider.check_proxy(True, '221.201.81.248:80')
