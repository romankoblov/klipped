#!/usr/bin/env python
# encoding: utf-8
"""
thread.py

Thread controller
"""

import tornado.web

class ThreadHandler(tornado.web.RequestHandler):
    """ Thread handler """
    def get(self, board, thread):
        """ Returns thread (list of posts) """
        self.write('Thread handler {board}/{thread}'.format(board=board, thread=thread))

    def post(self, board, thread):
        """ Adding new post to thread """
        pass
