import easydb.exception
from .exception import *
import string
import re

def iterable_check(obj):
    try:
        iter(obj)
    except TypeError:
        raise TypeError("item is not iterable")
        return False

def table_name_check(table_name, existing_table_names):
    #1.should be string; 
    if isinstance(table_name, str) == False:
        raise TypeError("table name is not a string: " + table_name)
        return False    
    #2.must start with a letter, followed by letters(either case), numbers, or underscore
    if table_name[0].isalpha() == False:
        raise ValueError("table name must start with a letter: " + table_name) 
        return False
    if re.match("^[A-Za-z0-9_]*$", table_name) == None:
        raise ValueError("table name must only contain letters, numbers and underscore: " + table_name)
        return False
    #3.cannot be duplicated
    for name in existing_table_names:
        if table_name == name:
            raise ValueError("duplicate table name: " + table_name)
            return False
    
def column_name_check(col_name, existing_column_names):
    #1.should be string; 
    if isinstance(col_name, str) == False:
        raise TypeError("column name is not a string: " + col_name)
        return False     
    #2.must start with a letter, followed by letters(either case), numbers, or underscore
    if col_name[0].isalpha() == False:
        raise ValueError("column name must start with a letter: " + col_name) 
        return False
    if re.match("^[A-Za-z0-9_]*$", col_name) == None:
        raise ValueError("column name must only contain letters, numbers and underscore: " + col_name)
        return False
    #3.cannot be "id"
    if col_name == "id":
        raise ValueError("column name is 'id'")
    #4.cannot be duplicated
    for name in existing_column_names:
        if col_name == name:
            raise ValueError("duplicate table name: " + col_name)
            return False
        
def column_type_check(col_type, table_index, existing_table_names):
    if isinstance(col_type, str):
    #1.cannot reference to current table
        if col_type == existing_table_names[table_index]:
            raise IntegrityError("foreign key causes a cycle: references to current table")
            return False
    #2.cannot reference to nonexistent table  
        if col_type not in existing_table_names:
            raise IntegrityError("foreign key references a nonexistent table")
            return False
    #3.should be one of str, float, int   
    elif col_type != str and col_type != int and col_type != float:
        raise ValueError("column type is not one of strng, float or integer")
        return False

def insert_check(table_name, values, table_names, table_col_count, col_type):
    if table_name not in table_names:
        raise PacketError("table name does not exist")
        return False
    table_index = table_names.index(table_name)

    if len(values) != table_col_count[table_index]:
        raise PacketError("doesn't match number of columns")
        return False

    for i in range(len(values)):
        if isinstance(col_type[table_index][i], str):
            if isinstance(values[i], int) == False:      #foreign field is not int
                raise InvalidReference("BAD_FOREIGN")
                return False
        elif isinstance(values[i], col_type[table_index][i]) == False:
            raise PacketError("column has an invalid type")
            return False
    return True

def update_check(table_name, pk, values, version, table_names, table_col_count, col_type):
    #Check everything that the insert command checks
    if insert_check(table_name, values, table_names, table_col_count, col_type) == False:
        return False
    #Check if row id is of type int
    if isinstance(pk, int) == False:
        raise PacketError('row id must be of type int')
        return False
    #Check if version is of type int
    if isinstance(version, int) == False:
        raise PacketError('version must be of type int')
        return False
    
    return True

def drop_check(table_name, pk, table_names, table_row_count):
    #Check if table name exists
    if table_name not in table_names:
        raise PacketError('table does not exist')
        return False
    #Check if row id is of type int
    if isinstance(pk, int) == False:
        raise PacketError('row id must be of type int')
        return False
    #Check if row id exists in the table
    num_rows = table_row_count[table_names.index(table_name)]
    if pk < 1 or pk > num_rows:
        raise ObjectDoesNotExist('row id does not exist in the table')
        return False

    return True

def get_check(table_name, pk, table_names, table_row_count):
    #Check if table name exists
    if table_name not in table_names:
        raise PacketError('table does not exist')
        return False
    #Check if row id is of type int
    if isinstance(pk, int) == False:
        raise PacketError('row id must be of type int')
        return False
    #Check if row id exists in the table
    num_rows = table_row_count[table_names.index(table_name)]
    if pk < 1 or pk > num_rows:
        raise ObjectDoesNotExist('row id does not exist in the table')
        return False

    return True

