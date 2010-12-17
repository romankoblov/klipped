#!/usr/bin/env python
# encoding: utf-8
"""
thread.py

Thread model
"""
import models

class ThreadModel(models.Model):
    def __init__(self, *args, **kwargs):
        self.fields = ['id', 'author', 'title', 'body', 'email', 'image']
        super(ThreadModel, self).__init__(*args, **kwargs)
