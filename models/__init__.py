#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py
"""
class Item(object):
    def __init__(self, table, **kwargs):
        self.model = model
        self.values = {}
        self.slots_values = {}
        for field in kwargs:
            if field in self.model.fields:
                if self.model.fields[field] is not None:
                    self.values[field] = self.model.fields[field](kwargs[field])
                else:
                    self.values[field] = kwargs[field]
        for field in kwargs:
            if field in self.table.slots:
                self.__setattr__(field, kwargs[field])

    def save(self):
        # Update existing
        if self.id:
            self.model.update(self)
        # Adding new
        else:
            id = self.model.insert(self)
            self.id = id
    
    def destroy(self):
        """docstring for destroy"""
        if self.id:
            self.table.destroy(self.id)

    def __setattr__(self, attr, value):
        # Update class attrs by default method
        if attr in ['table', 'values', 'slots_values']:
            return object.__setattr__(self, attr, value)
        # Update item fields by this:
        if attr in self.model.fields:
            if self.model.fields[attr] is not None:
                self.values[attr] = self.model.fields[attr](value)
            else:
                self.values[attr] = value
        # Update slot:
        if attr in self.table.slots:
            slot = getattr(self.table, attr)
            return slot(self, value)

    def __getattr__(self, attr):
        # Getting id field
        if attr in 'id':
            return self.values.get(self.table.pk, None)
        # Getting field
        if attr in self.model.fields:
            return self.values.get(attr, None)
        # Getting slot
        if attr in self.model.slots:
            slot = getattr(self.table, attr)
            return slot(self)

    def __str__(self):
        return '{self.model} #{self.id}'.format(self=self)
    __repr__ = __str__

class Model(object):
    def __init__(self, app, **kwargs):
        self.app = app
        if not self.fields:
            self.fields = []

    def get(self, **kwargs):
        """ Getting element from table """
        query = dict([(field, kwargs[field]) for field in kwargs if field in self.fields])
        #items = self.db.select(self.table, query, 1)
        if len(items) > 0:
            return Item(self, **items[0])
        else:
            return None

    def all(self, **kwargs):
        """ Return all elements of table """
        query = dict([(field, kwargs[field]) for field in kwargs if field in self.fields])
        #items = self.db.select(self.table, query)
        return [Item(self, **item) for item in items]

    def new(self, **kwargs):
        """ Return new element object """
        params = dict([(field, kwargs[field]) for field in kwargs if (field in self.fields) or (field in self.slots)])
        return Item(self, **params)

    def insert(self, item):
        """docstring for insert"""
        return self.db.insert(self.table, item.values)

    def update(self, item):
        """docstring for update"""
        self.db.update(self.table, {self.pk: item.id}, item.values)

    def destroy(self, id):
        """docstring for destroy"""
        self.db.execute("DELETE FROM `{table}` WHERE `{pk}` = '{id}'".format(table=self.table, pk=self.pk, id=id))

