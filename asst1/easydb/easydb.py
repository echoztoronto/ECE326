#!/usr/bin/python3
#
# easydb.py
#
# Definition for the Database class in EasyDB client
#

import sys
from .checks import *
import socket
import struct

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
		self.pk = 1                    # id of the row
		self.version = 0               # version of the row
		
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
			self.socket_obj = socket.socket()
			self.socket_obj.connect(self.address)
		except OSError as err:
			print(err)
			return False
		return True


	def close(self):
		#self.socket_obj.send(#should send EXIT or 6 here)  TODO!!!
		self.socket_obj.shutdown(2)
		self.socket_obj.close()
		#sys.exit(0)
		pass

	def insert(self, table_name, values):
		if insert_check(table_name, values, self.table_names, self.table_col_count, self.col_type) != False:
			self.pk += 1
			#to do: send to server, receive from server, also version = ?
		return (self.pk, self.version)

	def update(self, table_name, pk, values, version=None):
		# TODO: implement me
		pass

	def drop(self, table_name, pk):
		# TODO: implement me
		pass
		
	def get(self, table_name, pk):
		# TODO: implement me
		pass

	def scan(self, table_name, op, column_name=None, value=None):
		# TODO: implement me
		pass
                        
