# coding=utf-8
"""
This is for proxy server, avoid to ban the own ip.
"""

import urllib2

proxy_handler = urllib2.ProxyHandler({'http': '111.155.116.219:8123'})
opener = urllib2.build_opener(proxy_handler)
r = opener.open('http://www.silvercodingcat.com')
print r.read()
print 'go'
# 也可以用install_opener将配置好的opener安装到全局环境中，这样所有的urllib2.urlopen都会自动使用代理。

urllib2.install_opener(opener)
r = urllib2.urlopen('http://www.silvercodingcat.com')
print r.read()
