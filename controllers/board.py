#!/usr/bin/env python
# encoding: utf-8
"""
board.py

Board controller
"""

import tornado.web
import models.board

class BoardHandler(tornado.web.RequestHandler):
    """ Board handler """
    def get(self, board, format='html'):
        """ Returns list of threads in board """
        self.render("board.html", title="My title")

    def post(self, board, format='html'):
        """ Create new thread """
        pass
