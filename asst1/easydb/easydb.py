#!/usr/bin/python3
#
# easydb.py
#
# Definition for the Database class in EasyDB client
#

import sys
import socket
import struct
from .checks import *
from .helper import *
from .packet import *
from .exception import *

class Database:

    def __repr__(self):
        return "<EasyDB Database object>"

    def __init__(self, tables):
        self.schema = ()               # save it just in case
        self.table_names = []          # table_names[0] is table 1's name
        self.table_count = 0           # number of the tables
        self.table_col_count = []      # table_col_count[0] is the number of the columns in table 1
        self.column = []               # column[0][1] is column 2 of table 1
        self.col_type = []             # col_type[0][1] is the type of column 2 of table 1

        if iterable_check(tables) != False:                 #check if it's iterable
            self.schema = tables
            for table in tables:      
                if table_name_check(table[0],self.table_names) != False:       
                    self.table_names.append(table[0])       #save table name if valid
                    self.column.append([])
                    self.col_type.append([])
                    self.table_col_count.append(0)
                    for columns in tables[self.table_count][1]:
                        self.column[self.table_count].append([])
                        if column_name_check(columns[0],self.column[self.table_count]) != False:
                            self.column[self.table_count].append(columns[0])     #save column if valid
                            self.table_col_count[self.table_count] += 1
                        if column_type_check(columns[1],self.table_count,self.table_names) != False:
                            self.col_type[self.table_count].append(columns[1])   #save type if valid
                    self.table_count += 1

    def connect(self, host, port):
        self.address = (host, int(port))
        try:
            self.my_socket = socket.socket()
            self.my_socket.connect(self.address)
        except OSError as err:
            print(err)
            return False
        data = self.my_socket.recv(4096)
        error_code, = struct.unpack('!i', data)
        print(error_code)
        if error_code_check(error_code):
            return True
        else:
            self.my_socket.close()
            return False

    def close(self):
        self.my_socket.send(struct.pack("!ii", EXIT, 1)) 
        self.my_socket.shutdown(2)
        self.my_socket.close()

    def insert(self, table_name, values):
        #print(table_name)  #test
        #print(values)      #test
        if insert_check(table_name, values, self.table_names, self.table_col_count, self.col_type) != False:
            table_index = self.table_names.index(table_name)
            table_id =  table_index + 1
            num_elements = len(values) 
            sent_msg = b''.join([struct.pack('!i', INSERT), struct.pack('!i', table_id), struct.pack('!i', num_elements), pack_values(values, self.col_type[table_index])])
            self.my_socket.send(sent_msg)            
            data = self.my_socket.recv(4096)
            #print(data)  #test
            if len(data) == 20:
                error_code, self.pk, self.version, = struct.unpack('!iqq', data)
                if error_code_check(error_code):
                    return (self.pk, self.version)
            else:
                error_code, = struct.unpack('!i', data)
                if error_code_check(error_code) == False:
                    return False
            return True
        else:
            return False

    def update(self, table_name, pk, values, version=0):
        if update_check(table_name, pk, values, version, self.table_names, self.table_col_count, self.col_type) == True:
            
            packet = b''
            
            #Find table number
            table_num = self.table_names.index(table_name) + 1

            #struct request to binary
            packet += struct.pack('!ii', UPDATE, table_num)

            #struct key to binary
            packet += struct.pack('!qq', pk, version)

            #struct row to binary
            packet += struct.pack('!i', len(values)) + pack_values(values, self.col_type[table_num - 1])

            #Send to DB server and receive response
            self.my_socket.sendall(packet)
            resp = self.my_socket.recv(4096)

            #Check if response is OK
            if len(resp) != 4:
                resp = struct.unpack('!iq', resp)
                return resp[1]
            else:
                resp = struct.unpack('!i', resp)
                if resp[0] == NOT_FOUND:
                    raise ObjectDoesNotExist('NOT_FOUND')
                elif resp[0] == TXN_ABORT:
                    raise TransactionAbort('TXN_ABORT')
                else:
                    raise InvalidReference('BAD_FOREIGN')
                return

        else:
            return

    def drop(self, table_name, pk):
        if drop_check(table_name, pk, self.table_names) == True:

            packet = b''

            #Find table number
            table_num = self.table_names.index(table_name) + 1

            #struct request to binary
            packet += struct.pack('!ii', DROP, table_num)

            #long id to binary
            packet += struct.pack('!q', pk)

            #Send to DB server and receive response
            self.my_socket.sendall(packet)
            resp = self.my_socket.recv(4096)

            #Check if response is OK
            if struct.unpack('!i', resp) == OK:
                return
            else:
                raise ObjectDoesNotExist('NOT_FOUND')
                return

        else:
            return

    def get(self, table_name, pk):
        if get_check(table_name, pk, self.table_names) == True:

            packet = b''

            #Find table number
            table_num = self.table_names.index(table_name) + 1

            #struct request to binary
            packet += struct.pack('!ii', GET, table_num)

            #long id to binary
            packet += struct.pack('!q', pk)

            #Send to DB server and receive response
            self.my_socket.sendall(packet)
            resp = self.my_socket.recv(4096)

            #Check if response is OK
            if len(resp) != 4:
                # TODO: Unpack the response
                resp = resp[4:]
                version = struct.unpack('!q', resp[0:8])[0]
                resp = resp[8:]
                values = unpack_values(resp)

                return values, version
            else:
                raise ObjectDoesNotExist('NOT_FOUND')
                return

        else:
            return

    def scan(self, table_name, op, column_name=None, value=None):
        # TODO: implement me
        pass
                        
