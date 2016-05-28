class AlbumComment():
    """
    It represents the comment for an album, it is different than the entity in GAE
    """
    def __init__(self, comment, rank, user, album):
        self.album = album
        self.user = user
        self.rank = rank
        self.comment = comment