#!/usr/bin/env python
# encoding: utf-8
"""
board.py

Board model
"""
import models

class BoardModel(models.Model):
    def __init__(self, *args, **kwargs):
        self.fields = ['name']
        super(BoardModel, self).__init__(*args, **kwargs)


