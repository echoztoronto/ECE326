#!/usr/bin/python3
#
# table.py
#
# Definition for an ORM database table and its metaclass
#

from collections import OrderedDict
from .easydb import Database

# metaclass of table
# Implement me or change me. (e.g. use class decorator instead)
class MetaTable(type):

    #Keep track of tables already defined
    tables = []
    reserved_words = ['pk', 'version', 'save', 'delete']

    def __init__(cls, name, bases, attrs):
        MetaTable.tables.append(cls)
    
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
                if op not in ("ne", "gt", "lt", "eq"):
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
        self.saved = False
        self.pk = None      # id (primary key)
        self.version = None # version
        self.values = []
        #self.__dict__.update(kwargs)
        for col, val in kwargs.items():
            setattr(self, col, val)
            self.values.append(val)
        
        
    # Save the row by calling insert or update commands.
    # atomic: bool, True for atomic update or False for non-atomic update
    def save(self, atomic=True):
        if self.saved == False:  #not saved, do insert
            self.pk, self.version = self._db.insert(self.table_name, self.values)
        else:                    #saved, do update
            self.version = self._db.update(self.table_name, self.pk, self.values)
        
        self.saved = True
        
    # Delete the row from the database.
    def delete(self):
        self._db.drop(self.table_name, self.pk)
        
        self.pk = None
        self.version = None
        self.saved = False

