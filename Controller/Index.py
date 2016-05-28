import json
import webapp2
import Controller
import Libraries.Forza.Utils
import Libraries.bll
import Libraries.Model.Request
from datetime import datetime

# Constants
PageSize = 5


class Index(webapp2.RequestHandler, Controller.ControllerBase):
    """
    Load the main page, it is the first view
    """
    def get(self):
        order_by = self.request.get('order_by')
        if order_by is "" or not(order_by == "dtCreated" or order_by == "rank"):
            order_by = "dtCreated"
        template = self.JE.get_template('Index.html')
        #Retrieve the most popular tracks
        request = Libraries.Model.Request.TrackRequest(order_by="rank", top=6)
        tracks = Libraries.bll.get_track(request)
        #Retrieve the most popular albums
        request = Libraries.Model.Request.AlbumRequest(order_by="rank", top=6)
        albums = Libraries.bll.get_album(request)
        #Get the first comments according to the PageSize
        request = Libraries.Model.Request.CommentRequest(retrieve_all=True, order_by=order_by)
        comments = Libraries.bll.get_comments(request)
        #Update the dates to a more readily format
        for comment in comments:
            comment.dtCreated = Libraries.Forza.Utils.pretty_date(comment.dtCreated)
        context = {
            'comments': comments,
            'request': request,
            'orderBy': order_by,
            'tracks': tracks,
            'albums': albums
        }
        self.response.write(template.render(context))