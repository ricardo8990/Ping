class Album():
    """
    It represents an album is different than the entity in GAE
    """
    def __init__(self, name, artist, rank):
        self.name = name
        self.artist = artist
        self.rank = rank

        self.reviews = []
        self.urlId = ""
        self.dtCreated = ""
        self.number_comments = 0