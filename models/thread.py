#!/usr/bin/env python
# encoding: utf-8
"""
thread.py

Thread model
"""
import models

class ThreadModel(object):
    def __init__(self, *args, **kwargs):
        self.name = 'thread'#':b:111:author'
        self.fields = ['id', 'author', 'title', 'body', 'email', 'image']

