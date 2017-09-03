# coding=utf-8
"""
This is the main
"""

import json
import urllib
import urllib2
from encrypto import generate_data
from music import SongComment
from proxy_ip import ProxyIP


class CommentSpider(object):
    """
    Spider part
    """

    def __init__(self):
        pass

    __url_base = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_{0}/?csrf_token="

    __headers = {
        'Cookie': 'appver=1.5.0.75771;',
        'Referer': 'http://music.163.com/'
    }

    __DATA_MAX_LOOP = 10
    __DATA_MAX_CACHE = 10
    __data_loop = __DATA_MAX_LOOP
    __data_current = 0
    __data_list = []

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

    def get_request_url(self, song_id):
        """
        Get concat request url
        """
        return str.format(self.__url_base, song_id)

    def send_request(self, url, headers, data, proxy_ip=None):
        """
        Send comment request.
        """
        data = urllib.urlencode(data)
        request = urllib2.Request(url, data, headers)
        try:
            if proxy_ip is not None:
                proxy_data = {'http': proxy_ip.ip + ':' + proxy_ip.port}
                proxy_handler = urllib2.ProxyHandler(proxy_data)
                opener = urllib2.build_opener(proxy_handler)
                response = opener.open(request).read()
            else:
                response = urllib2.urlopen(request).read()
        except urllib2.URLError, error:
            response = None
            print error.message
        return response

    def get_response_comment(self, song_id, proxy_ip=None):
        """
        Send request and analysis response
        """
        comment = SongComment(song_id)
        response = self.send_request(self.get_request_url(comment.get_song_id(
        )), self.get_request_headers(), self.get_request_data(True), proxy_ip)
        if response is None:
            return None
        content = json.loads(response)
        comment.set_comment_total(content['total'])
        comment.set_comment_list(content['comments'])
        return comment


spider = CommentSpider()
print spider.get_response_comment('26584163').get_comment_total()
