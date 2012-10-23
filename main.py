import webapp2

from view.frontpage import FrontPage
from view.static import StaticFolder, StaticMarkdown

urls = [ (r'/', FrontPage), 
         (r'/s/([A-Za-z0-9-]+)', StaticFolder),
         (r'/s/([A-Za-z0-9-]+)/([A-Za-z0-9-]+)', StaticMarkdown),
]

application = webapp2.WSGIApplication(urls, debug=True)
