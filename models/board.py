#!/usr/bin/env python
# encoding: utf-8
"""
board.py

Board model
"""
import models

class BoardModel(object):
    def __init__(self, *args, **kwargs):
        self.name = 'board'
        self.fields = ['name']


