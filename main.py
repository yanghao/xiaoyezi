import webapp2

from view.static import StaticBlog

urls = [ (r'/blog/?([a-z]*)/?([A-Za-z0-9-]*)/?(.*)/?', StaticBlog),
]



application = webapp2.WSGIApplication(urls, debug=True)
