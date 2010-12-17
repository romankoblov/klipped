#!/usr/bin/env python
# encoding: utf-8
"""
thread.py

Thread controller
"""

import tornado.web
import models.thread

class ThreadHandler(tornado.web.RequestHandler):
    """ Thread handler """
    def get(self, board, thread, format='html'):
        """ Returns thread (list of posts) """
        posts = [{'id': 'id', 'author': 'author', 'title': 'title', 'body': 'body', 'email': 'email', 'image': 'image'}]
        self.write('Thread handler {board}/{thread}'.format(board=board, thread=thread))

    def post(self, board, thread, format='html'):
        """ Adding new post to thread """
        pass
