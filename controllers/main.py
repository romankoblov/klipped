#!/usr/bin/env python
# encoding: utf-8
"""
main.py

Main page controller
"""

import tornado.web

class MainHandler(tornado.web.RequestHandler):
    """ Main page handler """
    def get(self):
        """ Returns main page """
        self.write('Main handler')
