#!/usr/bin/env python2.6
# encoding: utf-8
"""
main.py

"""

import asyncmongo
import tornado.web

class Klipped(tornado.web.Application):
    """ Main application class """
    def __init__(self, routes={}, default_host="", transforms=None,
                     wsgi=False, **settings):
        """ Reinitializing Application.__init__ """
        super(Klipped, self).__init__(handlers=None, default_host="", transforms=None,
                         wsgi=False, **settings)

def main():
    application = Klipped()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
	main()

