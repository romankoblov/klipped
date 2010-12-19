#!/usr/bin/env python
# encoding: utf-8
"""
thread.py

Board controller
"""

import tornado.web
from brukva import adisp
from functools import partial
import simplejson
import time
import datetime

async = partial(adisp.async, cbname='callbacks')

def timestamp(datetime_obj):
    """ Convert datetime object to timestamp """
    if type(datetime_obj) is datetime.datetime:
        return int(time.mktime(datetime_obj.timetuple()))
    else:
        return int(datetime_obj)

class BoardHandler(tornado.web.RequestHandler):
    """ Board handler """
    @tornado.web.asynchronous
    @adisp.process
    def get(self, board, format='html'):
        """ Returns threads """
        (_, threads) = yield async(self.application.redis.zrevrange)("board:{board}:threads".format(board=board), 0, 10, with_scores=False)
        if not threads:
            threads = []
        if format == 'html':
            self.render("board.html", title="My title", threads=threads)
        elif format == 'json':
            pass

    @tornado.web.asynchronous
    @adisp.process
    def post(self, board, format='html'):
        """ Adding new thread to board """
        yield self.application.db.add_thread(board, self.request.arguments)
        self.redirect('/{board}.html'.format(board=board))