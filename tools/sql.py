from sqlite3 import Error
import sqlite3


class DataBase():
	def __init__(self, path):
		self.connection = None
		self.connection = sqlite3.connect(path)

	def write_query(self, query):
		self.cursor = self.connection.cursor()
		self.cursor.execute(query)
		self.connection.commit()

	def read_all_query(self, query):
		self.cursor = self.connection.cursor()
		self.result = self.cursor.execute(query)
		self.result = self.result.fetchall()
		self.cursor.close()
		return self.result

	def read_one_query(self, query):
		self.cursor = self.connection.cursor()
		self.result = self.cursor.execute(query)
		self.result = self.result.fetchone()
		self.cursor.close()
		return self.result