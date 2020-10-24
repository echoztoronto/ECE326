#!/usr/bin/python3
#
# orm.py
#
# Definition for setup and export function
#

from .easydb import Database
from .field import *
import sys, inspect

# Return a database object that is initialized, but not yet connected.
#   database_name: str, database name
#   module: module, the module that contains the schema
def setup(database_name, module):
    # Check if the database name is "easydb".
    if database_name != "easydb":
        raise NotImplementedError("Support for %s has not implemented"%(
            str(database_name)))
    
    tb_list = []
    table_count = 0

    for name, cls in module.__dict__.items():
        if inspect.isclass(cls):
            tb_list.append([name])
            attribute = []
            
            for attr, val in cls.__dict__.items():
                if not attr.startswith('__'):
                    if isinstance(val, Integer):
                        attribute.append((attr,int))
                    elif isinstance(val, Float):
                        attribute.append((attr,float))
                    elif isinstance(val, String):
                        attribute.append((attr,str))
                    elif isinstance(val, str):
                        attribute.append((attr,val))
                    elif isinstance(val, Coordinate):
                        attribute.append(("lat",float))
                        attribute.append(("lon",float))
                    elif isinstance(val, DateTime):
                        attribute.append((attr,float))
                        
            tb_list[table_count].append(tuple(attribute))
            table_count += 1
    
    tb = tuple(tuple(x) for x in tb_list)
    db = Database(tb)
    
    return db

# Return a string which can be read by the underlying database to create the 
# corresponding database tables.
#   database_name: str, database name
#   module: module, the module that contains the schema
def export(database_name, module):

    # Check if the database name is "easydb".
    if database_name != "easydb":
        raise NotImplementedError("Support for %s has not implemented"%(
            str(database_name)))
    result = ""
    
    for name, cls in module.__dict__.items():
        if inspect.isclass(cls):
            result.append(name)
            result.append(" {\n")
            
            for attr, val in cls.__dict__.items():
                if not attr.startswith('__'):
                    if isinstance(val, Integer):
                        result.append("\t" + attr + ": integer;\n")
                    elif isinstance(val, Float):
                        result.append("\t" + attr + ": float;\n")
                    elif isinstance(val, String):
                        result.append("\t" + attr + ": string;\n")
                    elif isinstance(val, str):
                        result.append("\t" + attr + ": " + str + ";\n")
                    # datetime and Coordinate????
            result.append("}\n")
    
    return result