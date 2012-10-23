import os
from webapp2 import RequestHandler, Response
from mako.template import Template

from view.cache import CacheHandler
from config import mc
from config import static_root
from config import template_root

class StaticFolder(CacheHandler):
    def __init__(self, request=None, response=None):
        CacheHandler.__init__(self, request, response, mc)

    def fetch_get_request(self, folder=''):
        t = Template(filename=os.path.join(template_root, 'base.html'))
        req_uri = self.request.path_info
        return t.render(req_uri=req_uri)

class StaticMarkdown(CacheHandler):
    def __init__(self, request=None, response=None):
        CacheHandler.__init__(self, request, response, mc)

    def fetch_get_request(self, folder='', filename=''):
        return 'folder: %s, filename: %s, path: %s' % (folder, filename, self.request.path_info)
