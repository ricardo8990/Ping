import json
import webapp2
import Controller
import Libraries.bll
import Libraries.Model.Track
import Libraries.Forza.Utils
import Libraries.Model.Request
from Libraries.Forza.Utils import *
from google.appengine.api import urlfetch


class Create(webapp2.RequestHandler, Controller.ControllerBase):
    """
    It creates a new Track, it must be used within an AJAX request and retrieves JSON data
    """
    def post(self):
        data = json.loads(self.request.body)
        name = str(data['name']).sanitize()
        artist = str(data['artist']).sanitize()
        album = data['album']
        #Validate that name, artist and album are not empty values, otherwise redirects to the main page
        if name is None or name.replace(" ", "") == "" or artist is None or artist.replace(" ", "") == "" or album is None:
           self.redirect("/")
           return
        #Validate if the track is already created, return the name and ID created
        request = Libraries.Model.Request.TrackRequest(name=name, artist=artist)
        track = Libraries.bll.get_track(request)
        if track != []:
            id_track = track[0].urlId
        else:
            id_track = Libraries.bll.save_track(Libraries.Model.Track.Track(artist, name, 0, album))
        track = {'name': name, 'id': id_track}
        self.response.out.write(json.dumps(track))


class Review(webapp2.RequestHandler, Controller.ControllerBase):
    """
    It is used for display information about an specific track, it requires the ulrId of the album as REST parameter
    """
    def get(self, track=None):
        context = {}
        order_by = self.request.get('order_by')
        #Order options are only dtCreated and rank if there is something else take date
        if order_by is "" or not(order_by == "dtCreated" or order_by == "rank"):
            order_by = "dtCreated"
        if track is None:
            self.redirect("/")
            return
        track_id = str(track).sanitize()
        #Get the track info
        request = Libraries.Model.Request.TrackRequest(url_id=track_id)
        track_obj = Libraries.bll.get_track(request)
        track_obj.dtCreated = Libraries.Forza.Utils.pretty_date(track_obj.dtCreated)
        #Get the reviews about the track
        request = Libraries.Model.Request.CommentRequest(track_id_url=track_id, order_by=order_by)
        comments = Libraries.bll.get_comments(request)
        for comment in comments:
            comment.dtCreated = Libraries.Forza.Utils.pretty_date(comment.dtCreated)
        #Get the image using Google Images
        image_url = None
        url = self.image_url.replace(self.replace_element, track_obj.artist.replace(" ", "%20"))
        json_data = urlfetch.fetch(url)
        data = json.loads(json_data.content)
        if "items" in data and len(data["items"]) > 0:
            image_url = data["items"][0]["link"]
        context = {
            'track': track_obj,
            'comments': comments,
            'orderBy': order_by,
            'image': image_url
        }
        template = self.JE.get_template('track.html')
        self.response.write(template.render(context))


class UpdateRank(webapp2.RequestHandler):
    """
    This method is used for update ranks and number of comments for each track, it must be used in a separated task due
    to it takes all existing tracks and calculate the average. So, it can take a while if there exists a lot of tracks
    """
    def get(self):
        #Get all tracks
        request = Libraries.Model.Request.TrackRequest(retrieve_all=True)
        tracks = Libraries.bll.get_track(request)
        for r in tracks:
            #Get all comments
            request = Libraries.Model.Request.CommentRequest(track_id_url=r.urlId)
            comments = Libraries.bll.get_comments(request)
            if len(comments) == 0:
                continue
            #Sum all ranks in comments and get average
            total_sum = sum([x.rank for x in comments])
            total = len(comments)
            r.rank = total_sum / total
            r.number_comments = total
            Libraries.bll.update_track(r)
        self.response.write("Done")


class Search(webapp2.RequestHandler):
    """
    Is used for search a track, parameter is the name of the track in a RESTFUL parameter, in case there is no query
    it will retrieve the first 50 tracks ordered by rank
    """
    def get(self, track=None):
        if track is None:
            request = Libraries.Model.Request.TrackRequest(order_by='rank', top=50)
        else:
            request = Libraries.Model.Request.TrackRequest(order_by='name', top=50, name=track)
        tracks = Libraries.bll.get_track(request)
        self.response.headers['Content-Type'] = 'application/json'
        objects = []
        for trk in tracks:
            objects.append({'track': trk.name, 'id': trk.urlId})
        self.response.out.write(json.dumps(objects))