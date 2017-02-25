import logging
import webapp2 as webapp
from google.appengine.ext import db

import blog_slugs

BLOG_HOME = 'http://blog.gregtracy.com'

# Data model to store request misses
class Miss(db.Model):
    request = db.StringProperty()
    counter = db.IntegerProperty(default=1)
##

def create_or_update(request):
    obj = db.GqlQuery("select * from Miss where request = :1", request).get()
    if not obj:
        obj = Miss()
        obj.request = request
    else:
        obj.counter += 1

    obj.put()
## end

class MainHandler(webapp.RequestHandler):

    def get(self, slug=None):
        if slug is not None and slug is not '':
            # strip off trailing slashes
            slug = slug.strip('/')

            # ignore requests for /posts/destroy
            if slug.find('posts/destroy') >= 0:
                self.redirect(BLOG_HOME)
                return

            # search for the slug in our lookup table
            slugs = blog_slugs.slugs.keys()
            if slug in slugs:
                new_slug = blog_slugs.slugs[slug]['new_slug']
                post_date = blog_slugs.slugs[slug]['date']
                if new_slug == '':
                    new_slug = slug + '.html'

                self.redirect('%s%s/%s' % (BLOG_HOME, post_date, new_slug))
            else:
                logging.debug('missed lookup for %s' % slug)
                create_or_update(slug)
                self.redirect(BLOG_HOME)

        else:
            self.redirect(BLOG_HOME)

        return

## end MainHandler

app = webapp.WSGIApplication([('/(.*)', MainHandler)])
