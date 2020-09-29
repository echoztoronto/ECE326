import struct
import string
from struct import (pack, unpack, calcsize)
from .packet import *

def pack_single_value(value, type): #pack a list of values
    if type == int:
        packed = pack("!iiq", INTEGER, 8, value)
    elif type  == float:
        packed = pack("!iid", FLOAT, 8, value)
    elif type  == str:
        length = len(value)
        size = nearest_4_multiples(length)
        fmt = "!ii" + str(length) + "s"
        packed = b''.join([pack(fmt, STRING, size, value.encode('ascii')), b'\x00'*(size-length)]) 
    else:
        packed = pack("!iiq", FOREIGN, 8, value)
    return packed
 
def pack_values(values, col_type): #pack a list of values
    packed = b''
    for i in range(len(values)):
        packed += pack_single_value(values[i], col_type[i])
    return packed
 
def nearest_4_multiples(x):
    if x%4 != 0:       
        return (x//4 + 1) * 4
    else:
        return x
