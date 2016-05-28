import Libraries.dao
import Libraries.Model.Request


# region Functions for comments

def get_comments(request):
    return Libraries.dao.get_track_comments(request)


def save_track_comment(comment):
    return Libraries.dao.save_track_comment(comment)


def get_album_comments(request):
    return Libraries.dao.get_album_comment(request)


def save_album_comment(comment):
    return Libraries.dao.save_album_comment(comment)


def delete_comment(request):
    return Libraries.dao.delete_track_comment(request)

# endregion


#region Functions for albums

def save_album(album):
    return Libraries.dao.save_album(album)


def get_album(request):
    return Libraries.dao.get_album(request)


def update_album(album):
    return Libraries.dao.update_album(album)
#endregion

# region Functions for tracks

def save_track(track):
    return Libraries.dao.save_track(track)


def get_track(request):
    return Libraries.dao.get_track(request)


def update_track(track):
    return Libraries.dao.update_track(track)

    # endregion


