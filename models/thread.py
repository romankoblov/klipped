#!/usr/bin/env python
# encoding: utf-8
"""
thread.py

Thread model
"""
import utils.model

class ThreadModel(object):
    def __init__(self, **kwargs):
        self.fields = ['id', 'author', 'title', 'body', 'email', 'image']
        super(ThreadModel, self).__init__(**kwargs)
