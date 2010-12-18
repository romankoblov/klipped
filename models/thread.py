#!/usr/bin/env python
# encoding: utf-8
"""
thread.py

Thread model
"""
#import models
# ./redis-cli incr next.news.id
# ./redis-cli set news:1:title "Redis is simple"
# ./redis-cli set news:1:url "http://code.google.com/p/redis"
# ./redis-cli lpush submitted.news 1

class ThreadModel(object):
    def __init__(self, app):
        self.app = app
        self.name = 'thread'#':b:111:author'
        self.fields = ['id', 'author', 'title', 'body', 'email', 'image']
        # keys:
        # board:b:id -- id
        # board:b:threads = list()
        # thread:b:333:posts_count = 22
        # post:b:111:43343:field = data
        # thread:b:222.posts = list()
    
    def add_thread(self, board, subject, text, mail=None, author=None, password=None, callback=None):
        """docstring for add_thread"""
        #Some validating
        # Get key
        params = {'board': board,
                  'subject': subject,
                  'text': text,
                  'mail': mail,
                  'author': author,
                  'password': password,
        }        
        id_key = "board:{board}:id".format(board=board)
        def incr_cb(result):
            (error, key) = result
            if not error:
                # There will be callback for error handling
                self.app.redis.rpush("board:{board}:threads".format(board=board), key)
                self.app.redis.incr("thread:{board}:{thread}:posts_counts".format(board=board, thread=key))
                data = {}
                for field in params:
                    data["post:{board}:{thread}:{post_id}:{field}".format(board=board, thread=key, post_id=key, field=field)] = params[field]
                self.app.redis.mset(data)
                self.app.redis.rpush("thread:{board}:{thread}:posts".format(board=board, thread=key), key)
        self.app.redis.incr(id_key, incr_cb)
        #print key

    def get_threads(self, board, start=0, stop=10, callback=None):
        def llen_cb(result):
            (error, threads_count) = result
            def lrange_cb(result):
                (error, threads) = result
                if callback:
                    callback(threads_count, threads)
            self.app.redis.lrange("board:{board}:threads".format(board=board), start, stop, lrange_cb)
        self.app.redis.llen("board:{board}:threads".format(board=board), llen_cb)

    def get_thread(self, board, thread):
        pass

    def get_key(board, thread, field):
        return "threads:{board}:{thread}:{field}"
    
