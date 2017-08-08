"""
This is timer comment spider
"""
# coding=utf-8

import time
from comment_spider import CommentSpider


def crawling(spider):
    """
    Send a crawling request.
    """
    return spider.get_response_comment().get_comment_total()


spider = CommentSpider('26584163')
current_total = crawling(spider)
aim_total = 8002
sleep_second = 30

while aim_total > current_total:
    print current_total
    time.sleep(sleep_second)
    current_total = crawling(spider)
print 'Bingo!'
