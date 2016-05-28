import webapp2
import Controller
import Libraries.bll
import Libraries.Forza.Utils
import Libraries.Model.Request
import Libraries.Model.TrackComment
import Libraries.Model.AlbumComment
from Libraries.Forza.Utils import *


class Create(webapp2.RequestHandler, Controller.ControllerBase):
    """
    This class is for creating a new review, the get method will show the main page and the post method is used
    for storing the data.
    """
    def get(self):
        template = self.JE.get_template('Create_review.html')
        context = {}
        self.response.write(template.render(context))

    def post(self):
        user = str(self.request.get('user')).sanitize()
        track = self.request.get('track')
        comment = str(self.request.get('comment')).sanitize()
        rank = int(self.request.get('rank'))
        #Validate that user, track, comment and rank are not empty
        if user is None or user.replace(" ", "") == "" or track is None or track.replace(" ", "") == "" \
                or comment is None or comment.replace(" ", "") == "":
            self.redirect("new_review")
            return
        track_comment = Libraries.Model.TrackComment.TrackComment(user, comment, rank, track)
        Libraries.bll.save_track_comment(track_comment)
        self.redirect("/review/track/" + track)


class CreateAlbum(webapp2.RequestHandler):
    """
    It creates a new album review and redirects to the album's page
    """
    def post(self):
        user = str(self.request.get('user')).sanitize()
        album = self.request.get('album')
        comment = str(self.request.get('comment')).sanitize()
        rank = int(self.request.get('rank'))
        #Validate that user, album and comment are not empty
        if user is None or user.replace(" ", "") == "" or album is None or album.replace(" ", "") == "" \
                or comment is None or comment.replace(" ", "") == "":
            self.redirect("/")
            return
        album_comment = Libraries.Model.AlbumComment.AlbumComment(comment, rank, user, album)
        Libraries.bll.save_album_comment(album_comment)
        self.redirect("/review/album/" + album)


class User(webapp2.RequestHandler, Controller.ControllerBase):
    """
    It shows the reviews created by the specified user
    """
    def get(self, user=None):
        context = {}
        order_by = self.request.get('order_by')
        #Order options are only dtCreated and rank if there is something else take date
        if order_by is "" or not(order_by == "dtCreated" or order_by == "rank"):
            order_by = "dtCreated"
        if user is not None:
            request = Libraries.Model.Request.CommentRequest(user=user, order_by=order_by)
            comments = Libraries.bll.get_comments(request)
            context = {'comments': comments, 'orderBy': order_by, 'user': user}
        template = self.JE.get_template('My_reviews.html')
        self.response.write(template.render(context))


class Delete(webapp2.RequestHandler):
    """
    Class used for delete a review. It will retrieve the author user id, only one comment can be retrieved at once.
    """
    def get(self, comment=None):
        if comment is None:
            self.redirect("/")
        request = Libraries.Model.Request.CommentRequest(comment=comment)
        comment_user = Libraries.bll.get_comments(request)
        if comment_user is None:
            self.redirect("/")
        else:
            Libraries.bll.delete_comment(request)
            self.redirect("/review/user/" + comment_user.user)