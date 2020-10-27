#!/usr/bin/python3
#
# table.py
#
# Definition for an ORM database table and its metaclass
#

from collections import OrderedDict
from .easydb import Database
from .field import *
from .orm import table_attributes, foreign_attributes, table_index
import inspect
from datetime import datetime

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
            
            for attr in attrs:
                if not attr.startswith('__'):
                    if attr is not None:
                        if attr[0].isalpha() == False:
                            raise AttributeError(attr + ' is an invalid column name')
                        for c in attr:
                            if c.isalnum() == False:
                                raise AttributeError(attr + ' is an invalid column name')

        return super().__new__(mcs, name, bases, attrs)


    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()

    # Returns an existing object from the table, if it exists.
    #   db: database object, the database to get the object from
    #   pk: int, primary key (ID)
    def get(cls, db, pk):
        result = db.get(cls.__name__, pk)

        values = result[0]
        version = result[1]

        attribute_list = table_attributes[cls.__name__]
        kwargs = {}
        value_index = 0

        for attr in attribute_list:
            if getattr(cls, attr).__class__.__name__ == 'Foreign':
                if values[value_index] == 0:
                    kwargs[attr] = None
                else:
                    kwargs[attr] = getattr(cls, attr).table.get(db, values[value_index])
                value_index += 1
                
            elif getattr(cls, attr).__class__.__name__ == 'DateTime':
                kwargs[attr] = datetime.fromtimestamp(values[value_index])
                
            elif getattr(cls, attr).__class__.__name__ == 'Coordinate':
                kwargs[attr] = (values[value_index], values[value_index+1])
                value_index += 1
                
            else:
                kwargs[attr] = values[value_index]
                value_index += 1

        table_object = cls(db, **kwargs)
        table_object.pk = pk
        table_object.version = version

        return table_object

    # Returns a list of objects that matches the query. If no argument is given,
    # returns all objects in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def filter(cls, db, **kwarg):
        pk_list = []
        result = []

        if kwarg == {}:
            scanned_pk = db.scan(cls.__name__, 1, None, None)
            if scanned_pk is not None:
                pk_list += scanned_pk   #no argument, returns all
            
        else:
            for columnname__op,value in kwarg.items():
                #split column and operator
                if columnname__op.find("__") == -1:
                    columnName = columnname__op
                    
                    if hasattr(cls, columnName) == False:
                        if columnName != "id":
                            raise AttributeError("column doesn't exist")
                    if columnName in foreign_attributes:
                        if not isinstance(value, int):
                            value = value.pk
                          
                    scanned_pk = db.scan(cls.__name__, 2, columnName, value)  #no underscore, equal     
                    if scanned_pk is not None:
                        pk_list += scanned_pk
                    
                else:
                    columnName, op = columnname__op.split("__")
                    
                    if hasattr(cls, columnName) == False:
                        if columnName != "id":
                            raise AttributeError("column doesn't exist")
                    if op not in ("ne", "gt", "lt"):
                        raise AttributeError("operator is not supported")
                        
                    if op == "ne":
                        operator = 3
                    elif op == "gt":
                        operator = 5
                    elif op == "lt":
                        operator = 4
                    
                    scanned_pk = db.scan(cls.__name__, operator, columnName, value)  #no underscore, equal     
                    if scanned_pk is not None:
                        pk_list += scanned_pk
                            
        if pk_list != []:
            for i in pk_list:
                result.append(cls.get(db, i))
        else:
            return None

        return result

    # Returns the number of matches given the query. If no argument is given, 
    # return the number of rows in the table.
    # db: database object, the database to get the object from
    # kwarg: the query argument for comparing
    def count(cls, db, **kwarg):
        result = cls.filter(db, **kwarg)
        if result is None:
            return 0
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
        self.attribute_list = table_attributes[self.table_name]
        
        for col, val in kwargs.items():
            setattr(self, col, val)
            self.defined_attr.append(col)
            self.defined_attr_dict[col] = val
                
        for attr in self.attribute_list:
              
            if attr in self.defined_attr:
                self.values.append(self.defined_attr_dict[attr])
            elif not attr.startswith("__") and not attr.startswith("_"):

                field = getattr(self.__class__, attr)
                
                if field.blank is False:
                    raise AttributeError("column value is not specified")
                else:
                    setattr(self, attr, field.default)
                    self.values.append(field.default)

        
    # Save the row by calling insert or update commands.
    # atomic: bool, True for atomic update or False for non-atomic update
    def save(self, atomic=True):
        
        values = []
        #Get the values for each column to save
        for attr in self.attribute_list:
            field = getattr(self.__class__, attr)

            if field.__class__.__name__ == 'DateTime':
                values.append(getattr(self, attr).timestamp())
            elif field.__class__.__name__ == 'Coordinate':
                values.append(float(getattr(self, attr)[0]))
                values.append(float(getattr(self, attr)[1]))
            elif field.__class__.__name__ == 'Foreign':
                if getattr(self, attr) is None:
                    values.append(0)
                elif getattr(self, attr).pk is None:
                    getattr(self, attr).save()
                    values.append(getattr(self, attr).pk)
                else:
                    values.append(getattr(self, attr).pk)
            else:
                values.append(getattr(self, attr))
        
        if not self.saved:  #not saved, do insert
            #raise ValueError("hi, this is what I'm inserting: ", self.table_name, values)
            self.pk, self.version = self._db.insert(self.table_name, values)
            self.saved = True
        else:               #saved, do update
            if atomic:
                self.version = self._db.update(self.table_name, self.pk, values, self.version)
            else:
                self.version = self._db.update(self.table_name, self.pk, values, 0)
        
    # Delete the row from the database.
    def delete(self):
        self._db.drop(self.table_name, self.pk)
        
        self.pk = None
        self.version = None
        self.defined_attr.clear()       
        self.defined_attr_dict.clear()
        self.values.clear()
        self.saved = False
        self.attribute_list.clear()
        