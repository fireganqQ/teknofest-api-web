import sqlite3 as sql


class allDataBase:
	def __init__(self, school_code):
		self.db = sql.connect("allDataBase.db3")
		self.cursor = self.db.cursor()

	def dbRead(self):
		try:
			get = self.cursor.execute("SELECT school_code FROM allDataBase")
		except TypeError:
			self.__dbCreate__()
			return [None]
		except sql.OperationalError:
			self.__dbCreate__()
			return [None]
		return get.fetchall()


	def __dbCreate__(self):
		self.cursor.execute("CREATE TABLE allDataBase (school_code)")
		self.db.commit()