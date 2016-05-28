
class Request():
    """
    Base class for each Request created, it contains general information as the order_by or top which means how many
    elements you want to receive. Pagination and cursor is also managed in this class.
    This requests help us to no create a specific query for each need, instead we will have a general query and
    fix the parameters in the request according to our needs.
    """
    def __init__(self, use_pagination=None, retrieve_all=None, page_size=10, order_by=None, order_asc=False, top=None, cursor=None):
        self.usePagination = use_pagination
        self.retrieveAll = retrieve_all
        self.pageSize = page_size
        self.order_by = order_by
        self.order_asc = order_asc
        self.cursor = cursor
        self.more = False
        self.top = top


class CommentRequest(Request):
    """
    This will be used to retrieve comments through the BLL. For instance, we can request all comments created by a
    user o with a specific rank.
    It is used for the TrackComment and AlbumComment entities in GAE
    """
    def __init__(self, comment=None, date_created=None, rank=None, user=None, track_id_url=None, album_id_url=None,
                 **kwargs):
        Request.__init__(self, **kwargs)
        self.comment = comment
        self.dtCreated = date_created
        self.rank = rank
        self.user = user
        self.track_id_url = track_id_url
        self.album_id_url = album_id_url


class TrackRequest(Request):
    """
    It's used for the Track entity in GAE
    """
    def __init__(self, artist=None, date_created=None, rank=None, url_id=None, album_id=None, name=None, **kwargs):
        Request.__init__(self, **kwargs)
        self.artist = artist
        self.dtCreated = date_created
        self.rank = rank
        self.url_id = url_id
        self.album_id = album_id
        self.name = name


class AlbumRequest(Request):
    """
    It's used for the Album entity in GAE
    """
    def __init__(self, name=None, artist=None, date_created=None, rank=None, url_id=None, **kwargs):
        Request.__init__(self, **kwargs)
        self.name = name
        self.artist = artist
        self.dtCreated = date_created
        self.rank = rank
        self.url_id = url_id