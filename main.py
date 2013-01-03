import webapp2
import logging

from view.static import StaticBlog

urls = [ (r'/blog/?([a-z]*)/?([A-Za-z0-9-]*)/?(.*)/?', StaticBlog),
]

logging.basicConfig(level=logging.DEBUG)

application = webapp2.WSGIApplication(urls, debug=True)
