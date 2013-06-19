
import sys, os
import os.path
import logging
import time

#os.environ['DJANGO_SETTINGS_MODULE'] = 'config'
from google.appengine.dist import use_library
use_library('django', '0.96')

#from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Dev')
if DEBUG: logging.getLogger().setLevel(logging.DEBUG)
logging.info('Loading %s, app version = %s',
             __name__, os.getenv('CURRENT_VERSION_ID'))


TEMPLATE_EXT = '.html'
TEMPLATE_DIR = 'views'


def _find_template(path):
    logging.debug('path: %s', path)
    if path in [None, '', '/']:
    	path = 'index'

    path = os.path.join( TEMPLATE_DIR, path + TEMPLATE_EXT )
    return path if os.path.exists(path) else None


def render( handler, page, params={} ):
    found_templ = _find_template(page)

    if found_templ is None:
        found_templ = _find_template( 'notfound' )
    
    # TODO memcache
    handler.response.out.write( template.render( 
            found_templ, params,
            debug=DEBUG ) )
        


class RequestHandler(webapp.RequestHandler):
    def get(self,path):
        logging.debug("RequestHandler#GET : /%s", path)
        render( self, 'index' )


    def post(self,path):
        logging.debug( "RequestHandler#POST : /%s : %s : %s", 
                path, self.request.content_type, self.request.body )
        self.response.set_status(201) # created
        self.response.headers['content_type'] = self.request.content_type
        self.response.out.write( self.request.body )


    def handle_exception(self, exception, debug_mode):
        if debug_mode:
            webapp.RequestHandler.handle_exception(self, exception, debug_mode)
        else:
            logging.exception(exception)
            self.error(500)


ROUTES = [
    ('/(.*)', RequestHandler) ]


def main():
    application = webapp.WSGIApplication(ROUTES, debug=DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__": main()
