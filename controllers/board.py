#!/usr/bin/env python
# encoding: utf-8
"""
board.py

Board controller
"""

import tornado.web

class BoardHandler(tornado.web.RequestHandler):
    """ Board handler """
    def get(self, board):
        """ Returns list of threads in board """
        self.write('Board handler {board}'.format(board=board))

    def post(self, board):
        """ Create new thread """
        pass
