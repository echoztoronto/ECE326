#!/usr/bin/python3
#
# orm.py
#
# Definition for setup and export function
#

from .easydb import Database
from .field import *
import sys, inspect

table_attributes = {}     

def getForeign(table, col):
    if col == "user":
        return "User"
    elif col == "location":
        if table == "Event":
            return "City"
        elif table == "Parade":
            return "Capital"


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
    table_attributes.clear()

    for name, cls in module.__dict__.items():
        if inspect.isclass(cls):
            tb_list.append([name])
            attribute = []
            attr_only = []  #only stores attr names, used for table_attributes
            
            for attr, val in cls.__dict__.items():
                if not attr.startswith('__'):
                    if isinstance(val, Integer):
                        attribute.append((attr,int))
                        attr_only.append(attr)
                        
                    elif isinstance(val, Float):
                        attribute.append((attr,float))
                        attr_only.append(attr)
                        
                    elif isinstance(val, String):
                        attribute.append((attr,str))
                        attr_only.append(attr)
                        
                    elif isinstance(val, Foreign):
                        attribute.append((attr, getForeign(name, attr)))
                        attr_only.append(attr)
                        
                    elif isinstance(val, Coordinate):
                        attribute.append((attr+"_lat",float))
                        attribute.append((attr+"_lon",float))
                        attr_only.append(attr)
                    
                    elif isinstance(val, DateTime):
                        attribute.append((attr,str))
                        attr_only.append(attr)
            
            table_attributes[name] = attr_only          
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
        if inspect.isclass(cls) and name not in ("datetime"):
            result += name
            result += " {\n"
            
            for attr, val in cls.__dict__.items():
                if not attr.startswith('__'):
                    if isinstance(val, Integer):
                        result += "\t" + attr + ": integer;\n"
                    elif isinstance(val, Float):
                        result += "\t" + attr + ": float;\n"
                    elif isinstance(val, String):
                        result += "\t" + attr + ": string;\n"
                    elif isinstance(val, Foreign):
                        result += "\t" + attr + ": " + getForeign(name, attr) + ";\n"  
                    elif isinstance(val, Coordinate):
                        result += "\t" + attr + "_lat: float;\n"
                        result += "\t" + attr + "_lon: float;\n"
                    elif isinstance(val, DateTime):
                        result += "\t" + attr + ": float;\n"
                    
            result += "}\n"
    
    return result
    

