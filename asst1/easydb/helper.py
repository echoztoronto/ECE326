import struct
import string
from struct import (pack, unpack, calcsize)
from .packet import *

    
def unpack_helper(fmt, data):
    size = calcsize(fmt)
    return unpack(fmt, data[:size])
    
def pack_values(values, table_names, col_type): #pack a list of values
    packed = b''
    for i in range(len(values)):
        if col_type[i] == int:
            packed += pack("!iiq", INTEGER, 8, values[i])
        elif col_type[i] == float:
            packed += pack("!iid", FLOAT, 8, values[i])
        elif col_type[i] == str:
            length = len(values[i])
            size = nearest_4_multiples(length)
            fmt = "!ii" + str(length) + "s"
            packed += b''.join([pack(fmt, STRING, size, values[i].encode('ascii')), b'\x00'*(size-length)]) 
        elif isinstance(col_type, str):
            packed += pack("!iiq", FOREIGN, 8, values[i])
    return packed
 
def nearest_4_multiples(x):
        return 4*round(x/4)
