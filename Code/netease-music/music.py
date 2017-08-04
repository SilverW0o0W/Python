"""
This is music information class
"""


class SongBase(object):
    """
    For base song information
    """

    def __init__(self):
        self.__song_id = '00000000'
        self.__artist_ids = ['00000']
        self.__album_id = '0000000'

    def set_song_id(self, song_id):
        """
        Set song id. Type: str
        """
        self.__song_id = song_id

    def get_song_id(self):
        """
        Get song id. Type: str
        """
        return self.__song_id

    def set_artist_ids(self, artist_ids):
        """
        Set artists id. Type: list str
        """
        self.__artist_ids = artist_ids

    def get_artist_ids(self):
        """
        Get artists id. Type: list str
        """
        return self.__artist_ids

    def set_album_id(self, album_id):
        """
        Set album id. Type: str
        """
        self.__album_id = album_id

    def get_album_id(self):
        """
        Get album id. Type: list str
        """
        return self.__album_id


class SongComment(SongBase):
    """
    For comment content uncomplete
    """

    def __init__(self):
        SongBase.__init__()
        self.__comment_total = 0
        self.__offset = 0
        self.__comment_list = '0'

    def set_comment_total(self, comment_total):
        """
        Set comment total. Type: number
        """
        self.__comment_total = comment_total

    def get_comment_total(self):
        """
        Get comment total. Type: number
        """
        return self.__comment_total

    def set_offset(self, offset):
        """
        Set comment offset. Type: number
        """
        self.__offset = offset

    def get_offset(self):
        """
        Get comment offset. Type: number
        """
        return self.__offset

    def set_comment_list(self, comment_list):
        """
        Set comment list. Type: list str
        """
        self.__comment_list = comment_list

    def get_comment_list(self):
        """
        Get comment list. Type: list str
        """
        return self.__comment_list
