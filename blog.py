import os
import webapp2
import jinja2
import time

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class Entry(db.Model):
    #id = db.ReferenceProperty()
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class MainPage(Handler):
    def render_blog(self, postid="", subject="", content="", error=""):
        entries = db.GqlQuery("SELECT * FROM Entry ORDER BY created DESC")

        self.render("blog.html", entries=entries, error=error)

    def get(self):
        self.render_blog()

class Newpost(Handler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            e = Entry(subject = subject, content = content)
            e.put()
            time.sleep(1) #sleep for 1 second

            self.redirect("/blog")
        else:
            error = "we need subject and content filled!!"
            self.render_blog(subject, content, error)

application = webapp2.WSGIApplication([('/blog', MainPage), ('/blog/newpost', Newpost)], debug=True)