#!/usr/bin/env python
# encoding: utf-8
"""
thread.py

Thread controller
"""

import tornado.web
from models.thread import ThreadModel

class ThreadHandler(tornado.web.RequestHandler):
    """ Thread handler """
    def get(self, board, thread, format='html'):
        """ Returns thread (list of posts) """
        posts = [ThreadModel(id='id', author='author', title='title', body='body', email='email', image='image')]
        self.render("thread.html", title="My title", posts=posts)

    def post(self, board, thread, format='html'):
        """ Adding new post to thread """
        pass
