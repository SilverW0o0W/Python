#coding = utf-8
"""
This is music information class
"""


class SongBase(object):
    """
    For base song information
    """

    def __init__(self, song_id=None, artist_ids=None, album_id=None):
        self.song_id = song_id
        self.artist_ids = artist_ids
        self.album_id = album_id


class SongComment(SongBase):
    """
    For comment content
    """

    def __init__(self, song_id=None, artist_ids=None, album_id=None):
        SongBase.__init__(self, song_id, artist_ids, album_id)
        self.comment_total = 0
        self.offset = 0
        self.comments = None
        self.hot_comments = None
        self.comment_more = False
        self.hot_comment_more = False


class SongHotComment(SongBase):
    """
    For hot comment content
    """

    def __init__(self, song_id=None, artist_ids=None, album_id=None):
        SongBase.__init__(self, song_id, artist_ids, album_id)
        self.comment_total = 0
        self.hot_comments = None
        self.hot_comment_more = False


class CommentDetail(object):
    """
    For single comment
    """

    def __init_(self, song_id, comment_id, is_replied, content, user_id, time, liked_count):
        self.song_id = song_id
        self.comment_id = comment_id
        self.is_replied = is_replied
        self.content = content
        self.user_id = user_id
        self.time = time
        self.liked_count = liked_count
