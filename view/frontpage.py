import webapp2

class FrontPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("This is the front page.")
