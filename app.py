#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, flash
from db import dataBase
from re import search as __search
import sqlite3 as sql, os, json as __json
auth_tokenList = os.getenv("auth_tokenList").replace(", ", " ").replace("  ", " ").split()
school_codeList = os.getenv("school_codeList").replace(", ", " ").replace("  ", " ").split()
authToken_schoolCode = __json.loads(os.getenv("authToken_schoolCode"))
app = Flask(__name__)
error_text = {
	"HANDLER": '{"ok":false,"code":404,"description":"Not Found Handler"}',
	"MAIN": '{"ok":false,"code":404,"description":"Not Found"}',
	"SCHOOL_CODE": '{"ok":true,"code":202,"description":"Available"}',
	"LOGIN": '{"ok":true,"code":200,"result":"Logged In"}',
	"PUSH": '{"ok":true,"code":200,"result":"Successfully Sent"}',
	b"UPDATE": '{"ok":true,"code":200,"result":"Successfully Updated"}',
	'READ': '{{"ok":true,"code":200,"result":{}}}',
	'302': '{"ok": false, "code":302,"description":"(Found) Previously[Moved Temporarily]"}',
	'202': '{"ok": false, "code":202,"description":"Unauthorized information"}'
}
# ============== READ ================== #
@app.route("/api/v1/<auth_token>/<school_code>/login/read/<_class>/", methods=["GET"])
def class_read(auth_token, school_code: str, _class: str):
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		if authToken_schoolCode[auth_token] == school_code:
			pass
		else:
			return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	__db__ = dataBase(school_code)
	read = __db__.__sqlRead__()
	if __search(str(_class).lower(), str(read).lower()):
		a = str(__db__.__classRead__(str(_class).lower()))
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["READ"].format(a)}</pre>';__db__.__close__()
	return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["MAIN"]}</pre>';__db__.__close__()
# ============== UPDATE_CLASS_DATA ================== #
@app.route("/api/v1/<auth_token>/<school_code>/login/update/class_data/<_class>/<lessonId>/<day1>/<day2>/<day3>/<day4>/<day5>/<day1Teacher>/<day2Teacher>/<day3Teacher>/<day4Teacher>/<day5Teacher>/", methods=["GET"])
def class_data_update(auth_token, school_code: str, _class:str, lessonId:str, day1:str, day2:str, day3:str, day4:str, day5:str, day1Teacher:str, day2Teacher:str, day3Teacher:str, day4Teacher:str, day5Teacher:str):
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	__db__ = dataBase(school_code)
	read = __db__.__sqlRead__()
	if __search(str(_class).lower(), str(read).lower()):
		if __search('\''+str(lessonId)+'\'', str(__db__.__data_query__(_class))):
			a = __db__.__data_update__(_class, lessonId, day1, day2, day3, day4, day5, day1Teacher, day2Teacher, day3Teacher, day4Teacher, day5Teacher)
			return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text[b"UPDATE"]}</pre>';__db__.__close__()
		else:
			return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["MAIN"]}</pre>';__db__.__close__()
	else:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["MAIN"]}</pre>';__db__.__close__()
	return __db__.__close__()
# ============== PUSH_CLASS_DATA_MIAN ================== #
@app.route("/api/v1/<auth_token>/<school_code>/login/push/class_data/<_class>/<lessonId>/<day1>/<day2>/<day3>/<day4>/<day5>/<day1Teacher>/<day2Teacher>/<day3Teacher>/<day4Teacher>/<day5Teacher>/", methods=["GET"])
def class_data(auth_token, school_code: str, _class:str, lessonId:str, day1:str, day2:str, day3:str, day4:str, day5:str, day1Teacher:str, day2Teacher:str, day3Teacher:str, day4Teacher:str, day5Teacher:str):
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	__db__ = dataBase(school_code)
	read = __db__.__sqlRead__()
	if __search(str(_class).lower(), str(read).lower()):
		if __search(str(lessonId), str(__db__.__data_query__(_class))):
			return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["302"]}</pre>';__db__.__close__()
		a = __db__.__Push__(_class, lessonId, day1, day2, day3, day4, day5, day1Teacher, day2Teacher, day3Teacher, day4Teacher, day5Teacher)
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["PUSH"]}</pre>';__db__.__close__()
	else:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["MAIN"]}</pre>';__db__.__close__()
	return __db__.__close__()
# ============== PUSH_CLASS_DATA_MIAN ================== #
@app.route("/api/v1/<auth_token>/<school_code>/login/push/class_data/", methods=["GET"])
def class_data_main():
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["LOGIN"]}</pre>'
# ============== PUSH ================== #
@app.route("/api/v1/<auth_token>/<school_code>/login/push/classes/<classes>", methods=["GET"])
def aac(auth_token, school_code: str, classes: str):
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	code = ""
	__db__ = dataBase(school_code)
	classesList = classes.replace("%20", "&").split("&")
	for i in classesList:
		code = __db__.__sqlCreateClasses__(str(i.replace("=", "")))
	for i in classesList:
		code = __db__.__dataEntryClassesallDataBase__(str(i.replace("=", "")))
	if code == 200:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["PUSH"]}</pre>';__db__.__close__()
	else:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["MAIN"]}</pre>';__db__.__close__()
# ============== PUSH ================== #
@app.route("/api/v1/<auth_token>/<school_code>/login/push/classes/", methods=["GET"])
def c(auth_token, school_code: str):
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["LOGIN"]}</pre>'
# ============== PUSH ================== #
@app.route("/api/v1/<auth_token>/<school_code>/login/push/", methods=["GET"])
def cs(auth_token, school_code: str):
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	code = 200
	if code == 200:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["PUSH"]}</pre>';__db__.__close__()
	else:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["MAIN"]}</pre>';__db__.__close__()
# ============== READ ================== #
@app.route("/api/v1/<auth_token>/<school_code>/login/read/", methods=["GET"])
def d(auth_token, school_code: str):
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	__db__ = dataBase(school_code)
	output = __db__.__sqlRead__()
	return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["LOGIN"]}</pre>'; __db__.__close__()
# ============== LOGIN ================== #
@app.route("/api/v1/<auth_token>/<school_code>/login/", methods=["GET"])
def f(auth_token, school_code: str):
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["LOGIN"]}</pre>'
# ============== SCHOOL_CODE ================== #
@app.route("/api/v1/<auth_token>/<school_code>/", methods=["GET"])
def g(auth_token, school_code: str):
	if auth_token not in auth_tokenList or school_code not in school_codeList:
		return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["202"]}</pre>'
	return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["SCHOOL_CODE"]}</pre>'
# ============== AUTH_TOKEN ================== #
@app.route("/api/v1/<auth_token>/", methods=["GET"])
def a(auth_token):
	return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["MAIN"]}</pre>'
# ============== MAİN ================== #
@app.route("/api/v1/", methods=["GET"])
def auth():
	return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["MAIN"]}</pre>'
@app.errorhandler(404)
def error_handler(e):
	return f'<pre style="word-wrap: break-word; white-space: pre-wrap;">{error_text["HANDLER"]}</pre>', 400

if __name__ == '__main__':
	app.run()
