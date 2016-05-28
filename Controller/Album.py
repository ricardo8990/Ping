import json
import webapp2
import Controller
import Libraries.bll
import Libraries.Model.Album
import Libraries.Forza.Utils
import Libraries.Model.Request
from Libraries.Forza.Utils import *
from google.appengine.api import urlfetch


class Create(webapp2.RequestHandler):
    """
    It creates a new Album, it must be used within an Ajax request and the return type is JSON
    """
    def post(self):
        data = json.loads(self.request.body)
        name = str(data['name']).sanitize()
        artist = str(data['artist']).sanitize()
        #Validate that name and artist are not empty values, otherwise redirects to the main page
        if name is None or name.replace(" ", "") == "" or artist is None or artist.replace(" ", "") == "":
           self.redirect("/")
           return
        #Validate if the album is already created, return the name and ID created
        request = Libraries.Model.Request.AlbumRequest(name=name, artist=artist)
        album = Libraries.bll.get_album(request)
        if album != []:
            id_album = album[0].urlId
        else:
            id_album = Libraries.bll.save_album(Libraries.Model.Album.Album(name, artist, 0))
        album = {'name': name, 'id': id_album}
        self.response.out.write(json.dumps(album))


class Review(webapp2.RequestHandler, Controller.ControllerBase):
    """
    It is used for display information about an specific album, it requires the ulrId of the album as REST parameter
    """
    def get(self, album=None):
        context = {}
        order_by = self.request.get('order_by')
        #Order options are only dtCreated and rank if there is something else take date
        if order_by is "" or not(order_by == "dtCreated" or order_by == "rank"):
            order_by = "dtCreated"
        if album is None:
            self.redirect("/")
            return
        album_id = str(album).sanitize()
        #Get the track info
        request = Libraries.Model.Request.AlbumRequest(url_id=album_id)
        album_obj = Libraries.bll.get_album(request)
        if album_obj == []:
            self.redirect("/")
            return
        album_obj.dtCreated = Libraries.Forza.Utils.pretty_date(album_obj.dtCreated)
        track_request = Libraries.Model.Request.TrackRequest(album_id=album)
        tracks = Libraries.bll.get_track(track_request)
        request = Libraries.Model.Request.CommentRequest(album_id_url=album_id, order_by=order_by)
        comments = Libraries.bll.get_album_comments(request)
        for comment in comments:
            comment.dtCreated = Libraries.Forza.Utils.pretty_date(comment.dtCreated)
        #Get the image using Google Images
        image_url = None
        url = self.image_url.replace(self.replace_element, album_obj.name.replace(" ", "%20"))
        json_data = urlfetch.fetch(url)
        data = json.loads(json_data.content)
        if "items" in data and len(data["items"]) > 0:
            image_url = data["items"][0]["link"]
        context = {
            'album': album_obj,
            'tracks': tracks,
            'comments': comments,
            'orderBy': order_by,
            'image': image_url
        }
        template = self.JE.get_template('album.html')
        self.response.write(template.render(context))


class UpdateRank(webapp2.RequestHandler):
    """
    This method is used for update ranks and number of comments for each album, it must be used in a separated task due
    to it takes all existing albums and calculate the average. So, it can take a while if there exists a lot of albums
    """
    def get(self):
        #Get all albums
        request = Libraries.Model.Request.AlbumRequest(retrieve_all=True)
        albums = Libraries.bll.get_album(request)
        for r in albums:
            #Get all comments
            request = Libraries.Model.Request.CommentRequest(album_id_url=r.urlId)
            comments = Libraries.bll.get_album_comments(request)
            if len(comments) == 0:
                continue
            #Sum all ranks in comments and get average
            total_sum = sum([x.rank for x in comments])
            total = len(comments)
            r.rank = total_sum / total
            r.number_comments = total
            Libraries.bll.update_album(r)
        self.response.write("Done")


class Search(webapp2.RequestHandler):
    """
    Is used for search an album, parameter is the name of the album in a RESTFUL parameter, in case there is no query
    it will retrieve the first 50 albums ordered by rank
    """
    def get(self, album=None):
        if album is None:
            request = Libraries.Model.Request.AlbumRequest(order_by='rank', top=50)
        else:
            request = Libraries.Model.Request.AlbumRequest(order_by='name', top=50, name=album)
        tracks = Libraries.bll.get_album(request)
        self.response.headers['Content-Type'] = 'application/json'
        objects = []
        for trk in tracks:
            objects.append({'album': trk.name, 'id': trk.urlId})
        self.response.out.write(json.dumps(objects))