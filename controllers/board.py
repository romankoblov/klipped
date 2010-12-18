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

async = partial(adisp.async, cbname='callbacks')

class BoardHandler(tornado.web.RequestHandler):
    """ Board handler """
    @tornado.web.asynchronous
    @adisp.process
    def get(self, board, format='html'):
        """ Returns threads """
        (_, thread_count) = yield async(self.application.redis.llen)("board:{board}:threads".format(board=board))
        (_, threads) = yield async(self.application.redis.lrange)("board:{board}:threads".format(board=board), 0, 10)
        self.render("board.html", title="My title", threads=threads, thread_count=thread_count)

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
        self.application.redis.rpush("board:{board}:threads".format(board=board), key)
        self.application.redis.incr("thread:{board}:{thread}:posts_counts".format(board=board, thread=key))
        data_post = {}
        self.application.redis.set("post:{board}:{thread}:{post_id}:json".format(board=board, thread=key, post_id=key), simplejson.dumps(data))
        self.application.redis.rpush("thread:{board}:{thread}:posts".format(board=board, thread=key), key)
        self.redirect('/{board}.html'.format(board=board))