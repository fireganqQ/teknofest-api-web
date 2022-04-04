import sqlite3 as sql
from .allDb import allDataBase
from re import search as re_search


class dataBase:
	def __init__(self, school_code: str) -> None:
		self.school_code = school_code
		self.db = sql.connect(f"{school_code}.db3")
		self.cursor = self.db.cursor()

	def __sqlRead__(self):
		try:
			self.cursor.execute("SELECT * FROM 'allDataBase'")
			get = self.cursor.fetchall()
		except Exception as r:
			return r
		if len(get) == 0:
			return 'None'
		else:
			return get

	def __classRead__(self, _class: str):
		try:
			self.cursor.execute(f"SELECT * FROM '{_class}'")
			a = self.cursor.fetchall()
			return a
		except sql.OperationalError as r:
			return "404"
		except Exception as e:
			return "404"

	def __Push__(self, _class: str, lessonId: str, day1: str, day2: str, day3: str, day4: str, day5: str, day1Teacher: str, day2Teacher: str, day3Teacher: str, day4Teacher: str, day5Teacher: str):
		try:
			self.cursor.execute("SELECT * FROM 'allDataBase'")
			a = self.cursor.fetchall()
			if re_search(_class.lower(), str(a).lower()):
				self.cursor.execute(f"INSERT INTO '{_class.lower()}' VALUES('{lessonId}', '{day1}', '{day2}', '{day3}', '{day5Teacher}', '{day5}', '{day1Teacher}', '{day2Teacher}', '{day3Teacher}', '{day4Teacher}', '{day5Teacher}')")
			else:
				return 404
		except TypeError:
			return 404
		except sql.OperationalError as r:
			return 404
		except Exception as e:
			return 404

		self.db.commit()
		return 200, "a"
	def __data_query__(self, _class: str):
		try:
			self.cursor.execute("SELECT * FROM '{}'".format(_class))
			return self.cursor.fetchall()
		except Exception as r:
			return r

	def __data_update__(self, _class: str, lessonId: str, day1: str, day2: str, day3: str, day4: str, day5: str, day1Teacher: str, day2Teacher: str, day3Teacher: str, day4Teacher: str, day5Teacher: str):
		try:
			self.cursor.execute(f"""UPDATE '{_class}' SET 'day1'=?,'day2'=?,'day3'=?,'day4'=?,'day5'=?,'day1Teacher'=?,'day2Teacher'=?,'day3Teacher'=?,'day4Teacher'=?,'day5Teacher'=? WHERE lessonId=?""", (day1,day2,day3,day4,day5,day1Teacher,day2Teacher,day3Teacher,day4Teacher,day5Teacher,lessonId))
			self.db.commit()
		except sql.OperationalError as r:
			if re_search("no such table:".lower(), str(r).lower()):
				return 404
			return 400
		except Exception as r:
			return 404
	def __sqlCreate__(self, name):
		try:
			self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {name.lower()} (classes)")
			self.db.commit()
			return 200
		except:
			return 404
	def __sqlCreateClasses__(self, name: str):
		try:
			self.cursor.execute("CREATE TABLE IF NOT EXISTS '{name}' (lessonId, day1, day2, day3, day4, day5, day1Teacher, day2Teacher, day3Teacher, day4Teacher, day5Teacher)".format(name=name.lower()))
			self.db.commit()
			return 200
		except Exception as r:
			return 404
	def __dataEntryClassesallDataBase__(self, classes: str):
		try:
			self.cursor.execute("SELECT * FROM 'allDataBase'")
			a = self.cursor.fetchall()
			if re_search(str(classes), str(a)):
				return 200
			else:
				self.cursor.execute(f"INSERT INTO 'allDataBase' VALUES('{classes}')")
				self.db.commit()
				return 200
		except sql.OperationalError as r:
			if re_search("no such table:".lower(), str(r).lower()):
				self.__sqlCreate__("allDataBase")
				self.cursor.execute(f"INSERT INTO 'allDataBase' VALUES('{classes}')")
				self.db.commit()
				return 200
			return 404
		except Exception as e:
			return 400
	def __close__(self):
		return self.db.close()