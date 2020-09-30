import struct
import string
from struct import (pack, unpack, calcsize)
from .packet import *


def pack_values(values, col_type): #pack a list of values
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
        else:
            packed += pack("!iiq", FOREIGN, 8, values[i])
    return packed
 
def nearest_4_multiples(x):
    if x%4 != 0:       
        return (x//4 + 1) * 4
    else:
        return x

def unpack_values(data):
    #Get number of elements in the row
    num_elements = struct.unpack('!i', data[0:4])[0]
    data = data[4:]

    values = []

    #Unpack the list of values in the row
    for element in range(0, num_elements):
        col_type = struct.unpack('!i', data[0:4])[0]
        data = data[4:]

        if col_type == INTEGER:
            data = data[4:]
            values.append(struct.unpack('!q', data[0:8])[0])

            if element != num_elements - 1:
                data = data[8:]
        elif col_type == FLOAT:
            data = data[4:]
            values.append(struct.unpack('!d', data[0:8])[0])

            if element != num_elements - 1:
                data = data[8:]
        elif col_type == STRING:
            size = struct.unpack('!i', data[0:4])[0]
            data = data[4:]

            values.append(struct.unpack('!' + str(size) + 's', data[0:size])[0].decode('ascii'))

            if element != num_elements - 1:
                data = data[size:]
        else:
            data = data[4:]
            values.append(struct.unpack('!q', data[0:8])[0])

            if element != num_elements - 1:
                data = data[8:]

    #Get rid of null characters for strings
    for element in range(0, num_elements):
        if isinstance(values[element], str) and values[element].find('\x00') != -1:
            pos = values[element].find('\x00')
            values[element] = values[element][0:pos]

    return values

