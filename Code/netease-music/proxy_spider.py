# coding=utf-8
"""
This is for crawling proxy ip from ip website.
"""

import urllib2
from bs4 import BeautifulSoup

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

"""
获取所有代理IP地址
"""


def get_proxy_ip():
    proxy = []
    for i in range(1, 2):
        try:
            url = 'http://www.xicidaili.com/nn/' + str(i)
            req = urllib2.Request(url, headers=header)
            res = urllib2.urlopen(req).read()
            soup = BeautifulSoup(res,"html.parser")
            ips = soup.findAll('tr')
            for x in range(1, len(ips)):
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + "\t" + tds[2].contents[0] + "\t" + tds[5].contents[0]
                print ip_temp
                proxy.append(ip_temp)
        except:
            continue
    return proxy

get_proxy_ip()