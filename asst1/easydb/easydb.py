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
        self.table_row_count = []	   # Number of rows in each table currently

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

        #All tables start with no rows
        for table_number in range(0, self.table_count):
            self.table_row_count.append(0)

    def connect(self, host, port):
        self.address = (host, int(port))
        try:
            self.my_socket = socket.socket()
            self.my_socket.connect(self.address)
        except OSError as err:
            print(err)
            return False
        self.connected = True
        return True

    def close(self):
        if self.connnected:
            self.my_socket.sendall(struct.pack(">i",EXIT)) 
            self.my_socket.shutdown(2)
            self.my_socket.close()
            sys.exit(0)
            self.connected = False

    def insert(self, table_name, values):
        if insert_check(table_name, values, self.table_names, self.table_col_count, self.col_type) != False:
            table_index = self.table_names.index(table_name)
            table_id =  table_index + 1
            num_elements = len(values)   #count in struct row
            sent_msg = b''.join([struct.pack('!i', INSERT), struct.pack('!i', table_id), struct.pack('!i', num_elements), pack_values(values, self.table_names, self.col_type[table_index])])
            print(sent_msg)
            self.my_socket.sendall(sent_msg)
            
            '''
            recv_msg = self.my_socket.recvfrom(4096)
            error_code, self.pk, self.version = unpack_helper("qqq", recv_msg)
            
            if error_check(error_code):
                return (self.pk, self.version)
            else:
                return False
            '''
            
        else: 
            return False

    def update(self, table_name, pk, values, version=0):
        # TODO: implement me
        if update_check(table_name, pk, values, version, self.table_names, self.table_col_count, self.col_type) == True:
            # TODO: send to server and receive response
            pass
        else:
            return False

    def drop(self, table_name, pk):
        # TODO: implement me
        if drop_check(table_name, pk, self.table_names, self.table_row_count) == True:
            # TODO: send to server and receive response
            pass
        else:
            return False

    def get(self, table_name, pk):
        # TODO: implement me
        if get_check(table_name, pk, self.table_names, self.table_row_count) == True:
            # TODO: send to server and receive response
            pass
        else:
            return False

    def scan(self, table_name, op, column_name=None, value=None):
        # TODO: implement me
        pass
                        
