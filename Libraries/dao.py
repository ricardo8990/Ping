import Libraries.Model.TrackComment
import Libraries.Model.Track
import Libraries.Forza.Utils
import Libraries.Model.Album
import Libraries.Model.AlbumComment
from Libraries.Forza.Utils import *
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor


class TrackComment(ndb.Model):
    """
    Track class for storing in GAE, all fields are required and Track is its parent
    """
    comment = ndb.TextProperty(required=True, indexed=True)
    dtCreated = ndb.DateTimeProperty(auto_now_add=True)
    rank = ndb.IntegerProperty(default=0, required=True)
    user = ndb.StringProperty(required=True)


class AlbumComment(ndb.Model):
    """
    This entity stores the comments for the albums and is ancestor of Album
    """
    comment = ndb.TextProperty(required=True)
    dtCreated = ndb.DateTimeProperty(auto_now_add=True)
    rank = ndb.IntegerProperty(default=0, required=True)
    user = ndb.StringProperty(required=True)


class Track(ndb.Model):
    """
    Data related to the tracks, ancestor of Album and parent of TrackComments
    """
    name = ndb.StringProperty(required=True)
    artist = ndb.StringProperty(required=True)
    dtCreated = ndb.DateTimeProperty(auto_now_add=True)
    rank = ndb.IntegerProperty(default=0)
    totalComments = ndb.IntegerProperty(default=0)


class Album(ndb.Model):
    """
    Store the data about the albums, we could call it like "super entity" due to all the rest of the entities will be
    ancestor of this one
    """
    name = ndb.StringProperty(required=True)
    dtCreated = ndb.DateTimeProperty(auto_now_add=True)
    artist = ndb.StringProperty(required=True)
    rank = ndb.IntegerProperty(default=0)
    totalComments = ndb.IntegerProperty(default=0)


# endregion
# region Functions for comments
def get_track_comments(request):
    """
    Retrieves a list of comments according to the request
    :param request: It contains all info needed to return
    :type request: Libraries.Model.Request.Request
    :return:List of comments
    :rtype:Libraries.Model.TrackComment
    """
    if request.comment is not None:
        q = ndb.Key(urlsafe=request.comment)
        q_comment = q.get()
        return q_comment
    query = "SELECT * FROM TrackComment "
    constraints = []

    if not request.retrieveAll:
        if request.dtCreated is not None:
            constraints.append("dtCreated = {}".format(request.dtCreated))
        if request.rank is not None:
            constraints.append("rank = {}".format(request.rank))
        if request.user is not None:
            constraints.append("user = '" + request.user + "'")
        if request.track_id_url is not None:
            q = ndb.Key(urlsafe=request.track_id_url)
            constraints.append(" ANCESTOR IS {}".format(q))

    if constraints:
        query = query + " WHERE " + " AND ".join(constraints)

    if request.order_by is not None:
        query += " ORDER BY " + request.order_by + " " + (" ASC " if request.order_asc else " DESC ")

    if request.usePagination:
        if request.cursor is not None:
            curs = Cursor(urlsafe=request.cursor)
            q, request.cursor, request.more = ndb.gql(query).fetch_page(request.pageSize, start_cursor=curs)
        else:
            q, request.cursor, request.more = ndb.gql(query).fetch_page(request.pageSize)
    else:
        q = ndb.gql(query)

    result = []
    for element in q:
        user = str(element.user).repair()
        comm = str(element.comment).repair()
        rank = element.rank
        track = element.key.parent().get()
        comment = Libraries.Model.TrackComment.TrackComment(user, comm, rank, element.key.parent().urlsafe(),
                                                            element.key.parent().parent().urlsafe())
        comment.artist_track = str(track.artist).repair()
        comment.name_track = str(track.name).repair()
        comment.dtCreated = element.dtCreated
        comment.url_id = element.key.urlsafe()
        result.append(comment)
    return result


def save_track_comment(comment):
    """
    Converts the parameter to a Entity class and store it in GAE
    :param comment: The comment to store
    :type comment: Libraries.Model.TrackComment
    :return:The id of the new comment
    :rtype:Int
    """
    key = ndb.Key(urlsafe=comment.track)
    track_comment = TrackComment(parent=key)
    track_comment.populate(
        comment=comment.comment,
        rank=comment.rank,
        user=comment.user
    )
    comment_id = track_comment.put()
    return comment_id.id()


def delete_track_comment(request):
    """
    Delete a comment, only one comment can be deleted per time
    :param request: It only takes the comment id from the request
    :type request: Libraries.Model.Request.CommentRequest
    :return:Nothing
    :rtype:
    :TODO: return a boolean value, confirming if the item was deleted
    """
    key = ndb.Key(urlsafe=request.comment)
    key.delete()
    return


def get_album_comment(request):
    """
    Return the comments for an album
    :param request: The information of the comments to be retrieved
    :type request: Libraries.Model.Request.CommentRequest
    :return:List of comments
    :rtype:Libraries.Model.AlbumComment
    """
    query = "SELECT * FROM AlbumComment "
    constraints = []

    if not request.retrieveAll:
        if request.comment is not None:
            constraints.append("comment = '" + request.comment + "'")
        if request.dtCreated is not None:
            constraints.append("dtCreated = {}".format(request.dtCreated))
        if request.rank is not None:
            constraints.append("rank = {}".format(request.rank))
        if request.user is not None:
            constraints.append("user = '" + request.user + "'")
        if request.album_id_url is not None:
            q = ndb.Key(urlsafe=request.album_id_url)
            constraints.append(" ANCESTOR IS {}".format(q))

    if constraints:
        query = query + " WHERE " + " AND ".join(constraints)

    if request.order_by is not None:
        query += " ORDER BY " + request.order_by + " " + (" ASC " if request.order_asc else " DESC ")

    if request.usePagination:
        if request.cursor is not None:
            q, request.cursor, request.more = ndb.gql(query).fetch_page(request.pageSize, request.cursor)
        else:
            q, request.cursor, request.more = ndb.gql(query).fetch_page(request.pageSize)
    else:
        q = ndb.gql(query)

    result = []
    for element in q:
        user = str(element.user).repair()
        comm = str(element.comment).repair()
        rank = element.rank
        comment = Libraries.Model.AlbumComment.AlbumComment(comm, rank, user, element.key.parent())
        comment.dtCreated = element.dtCreated
        result.append(comment)
    return result


def save_album_comment(comment):
    """
    Converts the comment into a AlbumComment entity and stores it in GAE
    :param comment: The comment to be stored
    :type comment: Libraries.Model.AlbumComment
    :return:The id created
    :rtype:str
    """
    key = ndb.Key(urlsafe=comment.album)
    album_comment = AlbumComment(parent=key)
    album_comment.populate(
        comment=comment.comment,
        rank=comment.rank,
        user=comment.user
    )
    album_comment_id = album_comment.put()
    return album_comment_id


# endregion

# region Functions for albums:

def save_album(album):
    """
    Convert the album into a Album entity and stores it in GAE
    :param album: The album to be stored
    :type album: Libraries.Model.Album
    :return:The url for the entity key created
    :rtype:str
    """
    # Create object for gae store
    gae_album = Album()
    gae_album.populate(
        name=album.name,
        artist=album.artist,
        rank=album.rank if album.rank is not None else 0
    )
    gae_album_id = gae_album.put()
    return gae_album_id.urlsafe()


def get_album(request):
    """
    Retrieves a list of albums related to the request
    :param request: Contains the data to be retrieved
    :type request: Libraries.Model.Request.AlbumRequest
    :return:List of Albums
    :rtype:Libraries.Model.Album
    """
    if request.url_id is not None:
        q = ndb.Key(urlsafe=request.url_id)
        q_track = q.get()
        return get_album_from_result(q_track)

    query = "SELECT * FROM Album "
    constraints = []

    if not request.retrieveAll:
        if request.name is not None:
            constraints.append("name >= '" + request.name + "' AND name < '" + request.name + u"\ufffd'")
        if request.artist is not None:
            constraints.append("artist = '" + request.artist + "'")
        if request.dtCreated is not None:
            constraints.append("dtCreated = {}".format(request.dtCreated))
        if request.rank is not None:
            constraints.append("rank = {}".format(request.rank))

    if constraints:
        query = query + " WHERE " + " AND ".join(constraints)

    if request.order_by is not None:
        query += " ORDER BY " + request.order_by + " " + (" ASC " if request.order_asc else " DESC ")

    if request.top is not None:
        query += " LIMIT {}".format(request.top)

    if request.usePagination:
        if request.cursor is not None:
            q, request.cursor, request.more = ndb.gql(query).fetch_page(request.pageSize, request.cursor)
        else:
            q, request.cursor, request.more = ndb.gql(query).fetch_page(request.pageSize)
    else:
        q = ndb.gql(query)

    result = []
    for element in q:
        result.append(get_album_from_result(element))
    return result


def update_album(album):
    """
    Update the information about a specific album
    :param album: Album must contain in urlId the url key to be updated
    :type album: Libraries.Model.Album
    """
    q = ndb.Key(urlsafe=album.urlId)
    q_album = q.get()
    q_album.name = album.name
    q_album.artist = album.artist
    q_album.rank = album.rank
    q_album.totalComments = album.number_comments
    q_album.put()


def get_album_from_result(element):
    """
    Convert the entity "element" into a Album instance
    :param element: Entity
    :type element: Album
    :return:the instance of album
    :rtype:Libraries.Model.Album
    """
    url_id = element.key.urlsafe()
    artist = str(element.artist).repair()
    name = str(element.name).repair()
    rank = element.rank
    album = Libraries.Model.Album.Album(name, artist, rank)
    album.dtCreated = element.dtCreated
    album.urlId = url_id
    album.number_comments = element.totalComments
    return album


# endregion


# region Functions for tracks
def save_track(track):
    """
    Converts the track into a entity and stores it in GAE
    :param track: The track to be stored
    :type track: Libraries.Model.Track
    :return:The url of the key created
    :rtype:str
    """
    key = ndb.Key(urlsafe=track.album)
    gae_track = Track(parent=key)
    gae_track.populate(
        name=track.name,
        artist=track.artist,
        rank=track.rank if track.rank is not None else 0
    )
    gae_track_id = gae_track.put()
    return gae_track_id.urlsafe()


def get_track(request):
    """
    Retrieves a list of tracks according to the request
    :param request: The info to be retrieved
    :type request: Libraries.Model.Request.TrackRequest
    :return:List of tracks
    :rtype:Libraries.Model.Track
    """
    # if a URL key is specified ignore all the rest
    if request.url_id is not None:
        q = ndb.Key(urlsafe=request.url_id)
        q_track = q.get()
        return get_track_from_result(q_track)

    query = "SELECT * FROM Track "
    constraints = []

    if not request.retrieveAll:
        if request.artist is not None:
            constraints.append("artist = '" + request.artist + "'")
        if request.dtCreated is not None:
            constraints.append("dtCreated = {}".format(request.dtCreated))
        if request.rank is not None:
            constraints.append("rank = {}".format(request.rank))
        if request.album_id is not None:
            q = ndb.Key(urlsafe=request.album_id)
            constraints.append(" ANCESTOR IS {}".format(q))
        if request.name is not None:
            constraints.append("name >= '" + request.name + "' AND name < '" + request.name + u"\ufffd'")

    if constraints:
        query = query + " WHERE " + " AND ".join(constraints)

    if request.order_by is not None:
        query += " ORDER BY " + request.order_by + " " + (" ASC " if request.order_asc else " DESC ")

    if request.top is not None:
        query += " LIMIT {}".format(request.top)

    if request.usePagination:
        if request.cursor is not None:
            q, request.cursor, request.more = ndb.gql(query).fetch_page(request.pageSize, request.cursor)
        else:
            q, request.cursor, request.more = ndb.gql(query).fetch_page(request.pageSize)
    else:
        q = ndb.gql(query)

    result = []
    for element in q:
        result.append(get_track_from_result(element))
    return result


def update_track(track):
    """
    Updates the info of a track
    :param track: It must contain in urlId the url key entity to be stored
    :type track: Libraries.Model.Track
    """
    q = ndb.Key(urlsafe=track.urlId)
    q_track = q.get()
    q_track.name = track.name
    q_track.artist = track.artist
    q_track.rank = track.rank
    q_track.totalComments = track.number_comments
    q_track.put()


def get_track_from_result(element):
    """
    Returns
    :param element:
    :type element:
    :return:
    :rtype:
    """
    url_id = element.key.urlsafe()
    album = element.key.parent().get()
    artist = str(element.artist).repair()
    name = str(element.name).repair()
    rank = element.rank
    track = Libraries.Model.Track.Track(artist, name, rank, element.key.parent().urlsafe())
    track.album_name = album.name
    track.dtCreated = element.dtCreated
    track.urlId = url_id
    track.number_comments = element.totalComments
    return track

    # endregion