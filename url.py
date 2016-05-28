import webapp2
import Controller.Index
import Controller.Review
import Controller.Album
import Controller.Track


urls = [
    ('/?', Controller.Index.Index),
    ('/new/review/?', Controller.Review.Create),
    ('/new/review-album/?', Controller.Review.CreateAlbum),
    ('/new/album/?', Controller.Album.Create),
    ('/new/track/?', Controller.Track.Create),
    ('/review/user/?', Controller.Review.User),
    ('/review/user/(?P<user>[a-z A-Z 0-9 _-]+)/?', Controller.Review.User),
    ('/review/track/?', Controller.Track.Review),
    ('/review/track/(?P<track>[a-z A-Z 0-9 _-]+)/?', Controller.Track.Review),
    ('/review/album/?', Controller.Album.Review),
    ('/review/album/(?P<album>[a-z A-Z 0-9 _-]+)/?', Controller.Album.Review),
    ('/review/delete/(?P<comment>[a-z A-Z 0-9 _-]+)/?', Controller.Review.Delete),
    ('/tasks/track', Controller.Track.UpdateRank),
    ('/tasks/album', Controller.Album.UpdateRank),
    ('/search/track/?', Controller.Track.Search),
    ('/search/track/(?P<track>[a-z A-Z 0-9 _-]+)/?', Controller.Track.Search),
    ('/search/album/?', Controller.Album.Search),
    ('/search/album/(?P<album>[a-z A-Z 0-9 _-]+)/?', Controller.Album.Search)
]

app = webapp2.WSGIApplication(urls, debug=True)