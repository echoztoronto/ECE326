#!/usr/bin/python3
#
# table.py
#
# Definition for an ORM database table and its metaclass
#

from collections import OrderedDict
from .easydb import Database
from .field import *
import inspect

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

            #Check column names
            for value,key in kwargs.items():
                if value[0].isalpha() == False:
                    raise AttributeError(value + ' is an invalid column name')
                for c in value:
                    if c.isalnum() == False:
                        raise AttributeError(value + ' is an invalid column name')

        return super().__new__(mcs, name, bases, attrs)


    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()

    # Returns an existing object from the table, if it exists.
    #   db: database object, the database to get the object from
    #   pk: int, primary key (ID)
    def get(cls, db, pk):
        result = db.get(cls.__name__, pk)
        print(result)
        return result

    # Returns a list of objects that matches the query. If no argument is given,
    # returns all objects in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def filter(cls, db, **kwarg):
        result = list()
        if kwarg is None:
            result.append(db.scan(cls.__name__, operator))
        else:
            for columnname__op,value in kwarg.items():
                op =""
                #split column and operator
                if columnname__op.find("__") == -1:
                    columnName = columnname__op
                else:
                    columnName, op = columnname__op.split("__")
                
                if hasattr(cls, columnName) == False:
                    raise AttributeError("column doesn't exist")
                if op not in ("ne", "gt", "lt"):
                    raise AttributeError("operator is not supported")
                    
                if op == "ne":
                    operator = 3
                elif op == "gt":
                    operator = 5
                elif op == "lt":
                    operator = 4
                else:
                    operator = 1
                
                result.append(db.scan(cls.__name__, operator, columnName, value))
            
        return result

    # Returns the number of matches given the query. If no argument is given, 
    # return the number of rows in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def count(cls, db, **kwarg):
        result = list()
        result = list()
        if kwarg is None:
            result.append(db.scan(cls.__name__, operator))
        else:
            for columnname__op,value in kwarg.items():
                op =""
                #split column and operator
                if columnname__op.find("__") == -1:
                    columnName = columnname__op
                else:
                    columnName, op = columnname__op.split("__")
                
                if hasattr(cls, columnName) == False:
                    raise AttributeError("column doesn't exist")
                if op not in ("ne", "gt", "lt", "="):
                    raise AttributeError("operator is not supported")
                    
                if op == "ne":
                    operator = 3
                elif op == "gt":
                    operator = 5
                elif op == "lt":
                    operator = 4
                else:
                    operator = 1
                
                result.append(db.scan(cls.__name__, operator, columnName, value))
        return len(result)

# table class
# Implement me.
class Table(object, metaclass=MetaTable):

    def __init__(self, db, **kwargs):
        self._db = db
        self.table_name = self.__class__.__name__
        self.pk = None               # id (primary key)
        self.version = None          # version
        self.defined_attr = []       # attributes which have values
        self.defined_attr_dict = {}
        self.values = []
        self.saved = False
        
        for col, val in kwargs.items():
            setattr(self, col, val)
            self.defined_attr.append(col)
            self.defined_attr_dict[col] = val
        
        for attr in dir(self):
            x = getattr(self, attr)   
            if attr in self.defined_attr:
                self.values.append(self.defined_attr_dict[attr])
            elif not attr.startswith("__") and not attr.startswith("_"):
                if isinstance(x, (Integer, Float, Foreign, String, DateTime, Coordinate)):
                    if x.blank is False:
                        raise AttributeError("column value is not specified")
                    else:
                        setattr(self, x, x.default)
                        self.values.append(x.default)
        
    # Save the row by calling insert or update commands.
    # atomic: bool, True for atomic update or False for non-atomic update
    def save(self, atomic=True):
        if not self.saved:  #not saved, do insert
            self.pk, self.version = self._db.insert(self.table_name, self.values)
            self.saved = True
        else:                    #saved, do update
            self.version = self._db.update(self.table_name, self.pk, self.values, 0)
        
    # Delete the row from the database.
    def delete(self):
        self._db.drop(self.table_name, self.pk)
        
        self.pk = None
        self.version = None
        self.defined_attr.clear()       
        self.defined_attr_dict.clear()
        self.values.clear()
        self.saved = False
        