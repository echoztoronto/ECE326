#!/usr/bin/python3
#
# easydb.py
#
# Definition for the Database class in EasyDB client
#

import sys
from .checks import *

class Database:
	schema = ()               # save it just in case
	table_name = []           # table_name[0] is the table 1's name
	table_count = 0           # number of the tables
	table_col_count = []      # table_col_count[0] is the number of the columns in table 1
	column = []               # column[0][1] is column 2 of table 1
	col_type = []             # col_type[0][1] is the type of column 2 of table 1

	def __repr__(self):
		return "<EasyDB Database object>"

	def __init__(self, tables):
		if iterable_check(tables) != False:                #check if it's iterable
			self.schema = tables
			for table in tables:      
				if table_name_check(table[0],self.table_name) != False:       
					self.table_name.append(table[0])       #save table name if valid
					self.column.append([])
					self.col_type.append([])
					self.table_col_count.append(0)
					for columns in tables[self.table_count][1]:
						self.column[self.table_count].append([])
						if column_name_check(columns[0],self.column[self.table_count]) != False:
							self.column[self.table_count].append(columns[0])     #save column if valid
							self.table_col_count[self.table_count] += 1
						if column_type_check(columns[1],self.table_count,self.table_name) != False:
							self.col_type[self.table_count].append(columns[1])   #save type if valid
					self.table_count += 1                                             
		pass
		
	def connect(self, host, port):
		# TODO: implement me
		return False

	def close(self):
		self.schema = None             
		self.table_name = None          
		self.table_count = None          
		self.table_col_count = None  
		self.column_all = None          
		self.column = None              
		self.col_type = None
		#sys.exit(0)
		pass

	def insert(self, table_name, values):
		# TODO: implement me
		pass

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
                        
