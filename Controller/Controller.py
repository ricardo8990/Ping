import os
import jinja2


class ControllerBase():
    """
    Base class for the controllers, this way we avoid to define the jinja2 environment in each controller as well as
    the folder to be used in the views.
    """
    def __init__(self):
        pass

    JE = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Views'))),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

    key = "AIzaSyBoJILq0LKjXWvC46d1Q_IK6VSL4Pk5nWo"
    cse_id = "000537226710042710869:xucrjgiwxrm"
    replace_element = "{QUERY}"
    image_url = "https://www.googleapis.com/customsearch/v1?key=" + key + "&cx=" + cse_id + \
                "&q=" + replace_element + "&searchType=image&fileType=jpg&imgSize=medium&alt=json"