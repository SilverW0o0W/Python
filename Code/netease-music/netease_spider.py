# coding=utf-8
"""
This is main controller for netease music comment spider
"""

from proxy_controller import ProxyController
from proxy_spider import ProxySpider
from comment_spider import CommentSpider

controller_proxy = ProxyController()
spider_proxy= ProxySpider()
spider_comment = CommentSpider('26584163')

ip_list = spider_proxy.get_proxy_ip()

for ip in ip_list:
    if ip.is_https == False:
        controller_proxy.add_proxy(ip)
    

