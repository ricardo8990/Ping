class TrackComment():
    """
    It represents the comment for a track, it is different than the entity in GAE
    """
    def __init__(self, user, comment, rank, track=0, album=0):
        self.track = track
        self.rank = rank
        self.comment = comment
        self.user = user
        self.album = album
        self.artist_track = ""
        self.name_track = ""
        self.dtCreated = ""
        self.url_id = ""