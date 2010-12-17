#!/usr/bin/env python
# encoding: utf-8
"""
board.py

Board model
"""

class BoardModel(object):
    def __init__(self, **kwargs):
        self.fields = ['name']
        super(ThreadModel, self).__init__(**kwargs)


