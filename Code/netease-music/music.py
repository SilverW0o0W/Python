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
