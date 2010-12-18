#!/usr/bin/env python
# encoding: utf-8
"""
board.py

Board model
"""
import models

class BoardModel(object):
    def __init__(self, app):
        self.app = app
        self.name = 'board'
        self.fields = ['name']


