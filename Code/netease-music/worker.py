"""
This is the main
"""
# coding=utf-8

import json
import requests
from encrypto import gen_data
from music import SongComment

class Worker(object):
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

    def get_request_data(self):
        """
        Get request encrypt data
        """
        return gen_data()

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

    def send_request(self, url, headers, data):
        """
        Send comment request.
        """
        return requests.post(url, headers=headers, data=data)

    def get_response_comment(self):
        """
        Send request and analysis response
        """
        response = self.send_request(self.get_request_url(self.__comment.get_song_id()),
                                     self.get_request_headers(), self.get_request_data())
        content = json.loads(response.content)
        self.__comment.set_comment_total(content['total'])
        self.__comment.set_comment_list(content['comments'])
        return self.__comment


worker = Worker('26584163')
comment = worker.get_response_comment()
print comment.get_comment_total()
