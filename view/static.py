from webapp2 import RequestHandler, Response

from view.cache import CacheHandler
from config import mc

class StaticFolder(CacheHandler):
    def __init__(self, request=None, response=None):
        CacheHandler.__init__(self, request, response, mc)

    def fetch_get_request(self, folder='', filename=''):
        return 'folder: %s, filename: %s, path: %s' % (folder, filename, self.request.path_info)

class StaticMarkdown(CacheHandler):
    def __init__(self, request=None, response=None):
        CacheHandler.__init__(self, request, response, mc)

    def fetch_get_request(self, folder='', filename=''):
        return 'folder: %s, filename: %s, path: %s' % (folder, filename, self.request.path_info)
