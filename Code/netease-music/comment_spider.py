# coding=utf-8
"""
This is the main
"""

import json
import urllib
import urllib2
from encrypto import generate_data
from music import SongComment
from proxy_controller import ProxyController


class CommentSpider(object):
    """
    Spider part
    """

    def __init__(self, song_id='00000000'):
        self.__comment = SongComment(song_id)

    __url_base = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{0}/?csrf_token="

    __headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
    }

    __proxy_controller = ProxyController()

    __DATA_MAX_LOOP = 10
    __DATA_MAX_CACHE = 10
    __data_loop = __DATA_MAX_LOOP
    __data_current = 0
    __data_list = []

    def reset_song_id(self, song_id):
        """
        Reset comment instance
        """
        self.__comment = SongComment(song_id)

    def get_request_headers(self):
        """
        Get request headers.
        """
        return self.__headers

    def get_request_data(self, once=True):
        """
        Get request encrypt data
        """
        if once:
            return generate_data()
        else:
            if self.__data_current >= self. __DATA_MAX_CACHE:
                self.__data_current = 0
                self.__data_loop += 1
            if self.__data_loop >= self. __DATA_MAX_LOOP:
                self.__data_list[:] = []
                for i in range(self.__DATA_MAX_CACHE):
                    self.__data_list.append(generate_data())
                self.__data_loop = 0
                self.__data_current = 0
            data = self.__data_list[self.__data_current]
            self.__data_current += 1
            return data

    def get_song_comment(self):
        """
        Get comment instance
        """
        return self.__comment

    def get_request_url(self, song_id):
        """
        Get concat request url
        """
        return str.format(self.__url_base, song_id)

    def send_request(self, url, headers, data, use_proxy=False):
        """
        Send comment request.
        """
        data = urllib.urlencode(data)
        request = urllib2.Request(url, data, headers)
        try:
            if use_proxy:
                proxy_data = {'http': '111.155.116.233:8123'}
                proxy_handler = urllib2.ProxyHandler(proxy_data)
                opener = urllib2.build_opener(proxy_handler)
                response = opener.open(request).read()
            else:
                response = urllib2.urlopen(request).read()
        except urllib2.URLError, error:
            response = ''
            print error.message
        return response

    def get_response_comment(self):
        """
        Send request and analysis response
        """
        response = self.send_request(self.get_request_url(self.__comment.get_song_id()),
                                     self.get_request_headers(), self.get_request_data(True))
        content = json.loads(response)
        self.__comment.set_comment_total(content['total'])
        self.__comment.set_comment_list(content['comments'])
        return self.__comment


spider = CommentSpider('26584163')
print spider.get_response_comment().get_comment_total()
