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
        (errors, key) = yield async(self.redis.incr)("board:{board}:id".format(board=board))
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
    def add_post(self, board, thread, post_data, callbacks):
        data = yield self.validate(board, post_data)
        self.insert_post(board, thread, data['id'], data)
        callbacks(True)
    
    @async
    @adisp.process
    def add_thread(self, board, post_data, callbacks):
        data = yield self.validate(board, post_data)
        # Adding thread to board sorted set (with sorting by timestamp)
        self.insert_thread(board, data['id'], data)
        callbacks(True)

    def insert_thread(self, board, key, post_data):
        # Adding thread to board sorted set (with sorting by timestamp)
        self.redis.zadd("board:{board}:threads".format(board=board), post_data['date'], post_data['id'])
        # Inserting post to thread
        self.insert_post(board, key, key, post_data)
    
    def insert_post(self, board, thread, key, post_data):
        # Serializing post data
        data = simplejson.dumps(post_data)
        # Insert post
        self.redis.set("post:{board}:{thread}:{post_id}:json".format(board=board, thread=thread, post_id=key), data)
        # Adding post to thread
        self.redis.rpush("thread:{board}:{thread}:posts".format(board=board, thread=thread), key)
        # Incriment thread's posts count
        self.redis.incr("thread:{board}:{thread}:posts_counts".format(board=board, thread=thread))
        # Upping thread
        self.redis.zrem("board:{board}:threads".format(board=board), thread)
        self.redis.zadd("board:{board}:threads".format(board=board), post_data['date'], thread)
