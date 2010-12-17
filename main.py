#!/usr/bin/env python2.6
# encoding: utf-8
"""
main.py

"""
import os

# Importing tornado's stuff
import asyncmongo
import tornado.httpserver
import tornado.ioloop
import tornado.web

# Import controllers
import controllers.main
import controllers.board
import controllers.thread

class Klipped(tornado.web.Application):
    """ Main application class """

def main():
    settings = {'debug': True,
                'template_path': os.path.join(os.path.dirname(__file__), "views")
    }
    # TODO: Fix regexps
    application = Klipped([
        (r"/", controllers.main.MainHandler),
        (r"/([a-z]+).([a-z]+)", controllers.board.BoardHandler),
        (r"/([a-z]+)/([0-9]+).([a-z]+)", controllers.thread.ThreadHandler),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()

