class Track():
    """
    It represents a track, it is different than the entity in GAE
    """
    def __init__(self, artist, name, rank, album):
        self.artist = artist
        self.name = name
        self.rank = rank
        self.album = album

        self.reviews = []
        self.urlId = ""
        self.dtCreated = ""
        self.number_comments = 0
        self.album_name = ""