#!/usr/bin/env python
# encoding: utf-8
"""
db.py

Simple class for acccess to redis db
"""

# Imports
import time
import datetime
import simplejson
from functools import partial
# Adisp
from brukva import adisp
async = partial(adisp.async, cbname='callbacks')

def timestamp(datetime_obj):
    """ Convert datetime object to timestamp """
    if type(datetime_obj) is datetime.datetime:
        return int(time.mktime(datetime_obj.timetuple()))
    else:
        return int(datetime_obj)

class KlippeDB(object):
    """docstring for """
    def __init__(self, client):
        self.redis = client
    
    @async
    @adisp.process
    def get_key(self, board, callbacks):
        (errors, key) = yield async(self.redis.incr)("b:{board}:id".format(board=board))
        if not errors:
            callbacks(key)

    @async
    @adisp.process    
    def validate(self, board, post_data, callbacks):
        data = dict()
        # TODO: Add some validations
        data['subject'] = post_data.get('subject', None)
        data['author'] = post_data.get('author', None)
        data['email'] = post_data.get('email', None)
        data['password'] = post_data.get('password', None)
        data['body'] = post_data.get('body', None)
        # Adding post info 
        data['id'] = yield self.get_key(board)
        data['date'] = timestamp(datetime.datetime.now())
        callbacks(data)

    @async
    @adisp.process
    def add_post(self, req, board, thread, post_data, callbacks):
        data = yield self.validate(board, post_data)
        for cache_type in self.post_cache(req, data):
            self.redis.set("p:{board}:{thread}:{post}:{cache_type}".format(board=board, thread=thread, cache_type=cache_type[0], post=data['id']), cache_type[1])
        self.insert_post(board, thread, data['id'], data)
        yield self.update_thread_cache(req, board, thread)
        callbacks(True)
    
    @async
    @adisp.process
    def add_thread(self, req, board, post_data, callbacks):
        data = yield self.validate(board, post_data)
        # Adding thread to board sorted set (with sorting by timestamp)
        for cache_type in self.post_cache(req, data, True):
            self.redis.set("t:{board}:{thread}:head:{cache_type}".format(board=board, thread=data['id'], cache_type=cache_type[0]), cache_type[1])
            if cache_type[0] == 'html':
                head_html = cache_type[1]
        thread_html = req.render_string("thread_last.html", head=head_html, posts=[])
        self.redis.set("t:{board}:{thread}:html".format(board=board,thread=data['id']), thread_html)
        self.insert_thread(board, data['id'], data)
        callbacks(True)

    def insert_thread(self, board, key, post_data):
        # Adding thread to board sorted set (with sorting by timestamp)
        self.redis.zadd("b:{board}:threads".format(board=board), post_data['date'], post_data['id'])
        # Inserting post to thread
        #self.insert_post(board, key, key, post_data)
    
    def insert_post(self, board, thread, key, post_data):
        # Adding post to thread
        self.redis.rpush("t:{board}:{thread}:posts".format(board=board, thread=thread), key)
        # Incriment thread's posts count
        self.redis.incr("t:{board}:{thread}:posts_counts".format(board=board, thread=thread))
        # Upping thread
        self.redis.zrem("b:{board}:threads".format(board=board), thread)
        self.redis.zadd("b:{board}:threads".format(board=board), post_data['date'], thread)

    def post_cache(self, req, post_data, head=False):
        # Generating cache
        if head:
            fn = "head_post.html"
        else:
            fn = "post.html"
        html = req.render_string(fn, post=post_data)
        json = simplejson.dumps(post_data)
        return [('html', html), ('json', json)]

    @async
    @adisp.process
    def update_thread_cache(self, req, board, thread, callbacks):
        (_, head) = yield async(self.redis.get)("t:{board}:{thread}:head:html".format(board=board, thread=thread))
        (_, posts_ids) = yield async(self.redis.lrange)("t:{board}:{thread}:posts".format(board=board, thread=thread), -5, -1)
        (_, posts) = yield async(self.redis.mget)(["p:{board}:{thread}:{pid}:html".format(board=board, thread=thread, pid=pid) for pid in posts_ids])
        html = req.render_string("thread_last.html", head=head, posts=posts)
        self.redis.set("t:{board}:{thread}:html".format(board=board, thread=thread), html)
        callbacks(True)
