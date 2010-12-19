#!/usr/bin/env python2.6
# encoding: utf-8
"""
main.py

"""
import os

# Importing tornado's stuff
#import asyncmongo
import brukva
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
from tornado.options import define, options

# Import controllers
import controllers.main
import controllers.board
import controllers.thread

# Import models
import db


# Options defines
define("host", default='127.0.0.1', help="run on the given address", type=str)
define("port", default=8888, help="run on the given port", type=int)
define("debug", default=False, help="debug mode", type=bool)
define("mobile", default=False, help="mobile version", type=bool)
# Redis
define("redis_host", default='localhost', help="redis host", type=str)
define("redis_port", default=6379, help="redis port", type=int)
define("redis_password", default='', help="redis password", type=str)


class Klipped(tornado.web.Application):
    """ Main application class """
    def __init__(self):
        # Redis
        self.redis = brukva.Client(host=options.redis_host, port=options.redis_port, password=options.redis_password, reconnect=True)
        self.redis.connect()
        # Models
        self.db = db.KlippeDB(self.redis)
        # Routes
        # TODO: Fix regexps
        handlers = [
            (r"/", controllers.main.MainHandler),
            (r"/([a-z]+).([a-z]+)", controllers.board.BoardHandler),
            (r"/([a-z]+)/([0-9]+).([a-z]+)", controllers.thread.ThreadHandler),
        ]
        # Settings
        settings = {'debug': options.debug,
                    'template_path': os.path.join(os.path.dirname(__file__), "views/default")
        }
        if options.mobile:
            settings['template_path'] = os.path.join(os.path.dirname(__file__), "views/mobile")
        super(Klipped, self).__init__(handlers=handlers, **settings)

    def listen(self, port, address="", **kwargs):
        """Starts an HTTP server for this application on the given port."""
        # Backported from tornado git
        from tornado.httpserver import HTTPServer
        server = HTTPServer(self, **kwargs)
        server.listen(port, address)

def main():
    tornado.options.parse_config_file("klipped.conf")
    tornado.options.parse_command_line()
    application = Klipped()
    application.listen(options.port, address=options.host)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()

