#!/usr/bin/env python
# encoding: utf-8
"""
board.py

Board controller
"""

import tornado.web

class BoardHandler(tornado.web.RequestHandler):
    """ Board handler """
    def get(self):
        """ Returns list of threads in board """
        pass

    def post(self):
        """ Create new thread """
        pass

