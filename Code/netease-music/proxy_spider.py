# coding=utf-8
"""
This is for crawling proxy ip from ip website.
"""

import urllib2
from bs4 import BeautifulSoup


class ProxySpider(object):
    """
    This is the class for crawling proxy id
    """
    __user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    __header = {}
    __header['User-Agent'] = __user_agent

    def get_proxy_ip(self, page_count=2):
        """
        Get proxy ip
        """
        proxy = []
        for i in range(1, page_count):
            try:
                url = 'http://www.xicidaili.com/nn/' + str(i)
                req = urllib2.Request(url, headers=self.__header)
                res = urllib2.urlopen(req).read()
                soup = BeautifulSoup(res, "html.parser")
                ips = soup.findAll('tr')
                for x in range(1, len(ips)):
                    ip = ips[x]
                    tds = ip.findAll("td")
                    is_https = tds[5].contents[0] == 'HTTPS'
                    ip_temp = ProxyIP(tds[1].contents[0],
                                      tds[2].contents[0], is_https)
                    print ip_temp.ip + '\t' + ip_temp.port + '\t' + str(ip_temp.is_https)
                    proxy.append(ip_temp)
            except Exception, ex:
                continue
        return proxy


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


proxy_spider = ProxySpider()
proxy_spider.get_proxy_ip(2)
