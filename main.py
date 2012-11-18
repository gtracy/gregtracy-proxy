import os
import logging
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

import blog_slugs

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
    def get(self,slug=None):
      if( slug is not None and slug is not '' ):
        slugs = blog_slugs.slugs.keys()
        if( slug in slugs ):
            new_slug = blog_slugs.slugs[slug]['new_slug']
            post_date = blog_slugs.slugs[slug]['date']
            if( new_slug == '' ):
              new_slug = slug

            self.redirect('http://blog.gregtracy.com/%s/%s.html' % (post_date,new_slug))
        else:
            logging.debug('missed lookup for %s' % slug)
            create_or_update(slug)
            self.redirect('http://blog.gregtracy.com')
      else:
        self.redirect('http://blog.gregtracy.com')

      return      

## end MainHandler

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    application = webapp.WSGIApplication([('/(.*)', MainHandler),
                                         ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
