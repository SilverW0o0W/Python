# coding=utf-8
"""
This is for proxy server, avoid to ban the own ip.
"""

import urllib2


class ProxySpider(object):

    __check_http_url = 'http://silvercodingcat.com/python/2017/08/09/Proxy-Spider-Check/'
    __check_https_url = ''

    def check_proxy(self, is_http, ip_port):
        """
        Check proxy available
        """

        transfer_method = 'http' if is_http else 'https'
        proxy_handler = urllib2.ProxyHandler({transfer_method: ip_port})
        opener = urllib2.build_opener(proxy_handler)
        response = opener.open(self.__check_http_url)
        if response == 200:
            return True
        else:
            return False
# 也可以用install_opener将配置好的opener安装到全局环境中，这样所有的urllib2.urlopen都会自动使用代理。

# urllib2.install_opener(opener)
# r = urllib2.urlopen('http://www.silvercodingcat.com')
# print r.read()


spider = ProxySpider()
spider.check_proxy(True, '221.201.81.248:80')
