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
        self.render("board.html", title="My title", threads=threads)

    @tornado.web.asynchronous
    @adisp.process
    def post(self, board, format='html'):
        """ Adding new thread to board """
        data = {}
        for field in ['subject', 'author', 'email', 'password', 'body']:
            if self.get_argument(field, None):
                data[field] = self.get_argument(field, None)
        self.set_header("Content-Type", "text/plain")
        
        (_, key) = yield async(self.application.redis.incr)("board:{board}:id".format(board=board))
        print key
        data['id'] = key
        self.application.redis.zadd("board:{board}:threads".format(board=board), timestamp(datetime.datetime.now()), key)
        self.application.redis.incr("thread:{board}:{thread}:posts_counts".format(board=board, thread=key))
        data_post = {}
        self.application.redis.set("post:{board}:{thread}:{post_id}:json".format(board=board, thread=key, post_id=key), simplejson.dumps(data))
        self.application.redis.rpush("thread:{board}:{thread}:posts".format(board=board, thread=key), key)
        self.redirect('/{board}.html'.format(board=board))