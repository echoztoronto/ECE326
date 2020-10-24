#!/usr/bin/python3
#
# table.py
#
# Definition for an ORM database table and its metaclass
#

from collections import OrderedDict

# metaclass of table
# Implement me or change me. (e.g. use class decorator instead)
class MetaTable(type):

    #Keep track of tables already defined
    tables = []
    reserved_words = ['pk', 'version', 'save', 'delete']

    def __init__(cls, name, bases, attrs):
        pass
    
    def __new__(mcs, name, bases, attrs, **kwargs):
        
        if name != 'Table':
            #Check if the table has already been defined
            if name in MetaTable.tables:
                raise AttributeError(name + ' table has already been defined')
            else:
                MetaTable.tables.append(name)

            #Check if the table class uses reserved words
            for word in MetaTable.reserved_words:
                if word in attrs.keys():
                    raise AttributeError(word + ' is a reserved word')

            # TODO: Check column names

        return super().__new__(mcs, name, bases, attrs)


    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()

    # Returns an existing object from the table, if it exists.
    #   db: database object, the database to get the object from
    #   pk: int, primary key (ID)
    def get(cls, db, pk):
        return None

    # Returns a list of objects that matches the query. If no argument is given,
    # returns all objects in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def filter(cls, db, **kwarg):
        return list()

    # Returns the number of matches given the query. If no argument is given, 
    # return the number of rows in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def count(cls, db, **kwarg):
        return list()

# table class
# Implement me.
class Table(object, metaclass=MetaTable):

    def __init__(self, db, **kwargs):
        self.pk = None      # id (primary key)
        self.version = None # version
        self.__dict__.update(kwargs)

    # Save the row by calling insert or update commands.
    # atomic: bool, True for atomic update or False for non-atomic update
    def save(self, atomic=True):
        pass
        
    # Delete the row from the database.
    def delete(self):
        pass

