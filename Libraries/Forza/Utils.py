# This class is for declare functions that can be helpful but are not part of the main operation
# i.e. it can be used with any other code or project, the intend is to prepare a helpful library
from datetime import datetime


class str(str):
    """
    It adds more functionality to the str class
    """
    def sanitize(self):
        """
        It is used to replace some elements in the string and prevent code injection
        :return:The string sanitized
        :rtype:str
        """
        string_sanitized = self
        string_sanitized = string_sanitized.replace("&", "_amp;")
        string_sanitized = string_sanitized.replace("'", "_apos;")
        string_sanitized = string_sanitized.replace("\\", "_quot;")
        string_sanitized = string_sanitized.replace("<", "_lt;")
        string_sanitized = string_sanitized.replace(">", "_gt;")
        return string_sanitized

    def repair(self):
        """
        It is used to convert the sanitized string into the original one
        :return:The string
        :rtype:str
        """
        string = self
        string = string.replace("_amp;", "&")
        string = string.replace("_apos;", "'")
        string = string.replace("_quot;", "\"")
        string = string.replace("_lt;", "<")
        string = string.replace("_gt;", ">")
        string = string.replace("_93;", "]")
        string = string.replace("_91;", "[")
        string = string.replace("_92;", "\\")
        string = string.replace("_61;", "=")
        string = string.replace("_47;", "/")
        string = string.replace("_35;", "#")
        string = string.replace("_36;", "$")
        return string


def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now()
    diff = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"