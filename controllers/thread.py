#!/usr/bin/env python
# encoding: utf-8
"""
thread.py

Thread controller
"""

import tornado.web

class ThreadHandler(tornado.web.RequestHandler):
    """ Thread handler """
    def get(self):
        """ Returns thread (list of posts) """
        pass

    def post(self):
        """ Adding new post to thread """
        pass
