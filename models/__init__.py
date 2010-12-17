#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py
"""

class Model(object):
    def __init__(self, app, **kwargs):
        self.app = app
        if not self.fields:
            self.fields = []
        self.data = {}
        for field in kwargs:
            if field in self.fields:
                self.data[field] = kwargs[field]

    def __setattr__(self, attr, value):
        if attr in ['data', 'fields', 'app']:
            return object.__setattr__(self, attr, value)
        if attr in self.table.fields:
            self.data[attr] = value

    def __getattr__(self, attr):
        if attr in self.fields:
            return self.data.get(attr, None)
