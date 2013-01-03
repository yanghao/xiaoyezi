from webapp2 import RequestHandler, Response
import logging

class CacheHandler(RequestHandler):
    def __init__(self, request=None, response=None, mc=None, ignore_trailing_slash=True):
        RequestHandler.__init__(self, request, response)
        self.ignore_trailing_slash = ignore_trailing_slash
        self.log = logging.getLogger(self.__class__.__name__)
        if mc == None:
            raise "No Memcache Client provided"
        else:
            self.mc = mc

    def __del__(self):
        pass

    def get(self, *args, **kargs):
        req_uri = self.request.path_info.encode('UTF-8')
        if req_uri.endswith('/'):
            req_uri = req_uri[:-1]
        value = self.mc.get(req_uri)
        if value != None: # cache hit
            self.log.info("Cache hit : %s" % req_uri)
        else: # cache miss
            self.log.info("Cache miss : %s" % req_uri)
            value = self.fetch_get_request(*args, **kargs)
            self.mc.set(req_uri, value)
        return Response(value)

