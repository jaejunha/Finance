# -*- coding: utf-8 -*-
import pymysql
import json
import datetime

CONST_HOST = 'localhost'
CONST_CHARSET = 'utf8mb4'

def checkDB():
	error = False
	file_json = open('db.json','r')
	json_data = json.load(file_json)
	str_id = json_data["ID"]
	str_pwd = json_data["PWD"]
	str_db = json_data["DB"]
	file_json.close()
	try:
		sql_con = pymysql.connect(host = CONST_HOST, user = str_id, password = str_pwd, db = str_db, charset=CONST_CHARSET)
	except pymysql.err.InternalError as e:
		if str(e).find("Unknown database") >= 0 :
			sql_con = pymysql.connect(host='localhost', user=json_data["ID"], password=json_data["PWD"], charset=CONST_CHARSET)
			sql_cur = sql_con.cursor()
			sql_query = "create database finance character set "+CONST_CHARSET
			sql_cur.execute(sql_query)
			sql_query = "alter database finance character set="+CONST_CHARSET+" collate="+CONST_CHARSET+"_unicode_ci"
			sql_cur.execute(sql_query)
			sql_con.commit()
			sql_con.close()
		else:
			error = True
	return str_id, str_pwd, str_db, error

def getToday():
	list_date =  str(datetime.datetime.now()).split(' ')[0].split('-')
	str_today = list_date[0] + list_date[1] + list_date[2]
	return str_today

def checkToday(db_id, db_pwd, db_db):
	sql_con = pymysql.connect(host = CONST_HOST, user = db_id, password = db_pwd, db = db_db, charset = CONST_CHARSET)
	sql_cur = sql_con.cursor()
	sql_query = "select * from date_today where int_date='"+getToday()+"'"
	try:
		sql_cur.execute(sql_query)
		sql_rows = sql_cur.fetchall()
		if len(sql_rows) > 0:
			return True 

	except pymysql.err.ProgrammingError as e:
		if(str(e).find("doesn't exist") >= 0):	
			sql_query = "create table date_today(int_date int, primary key(int_date));"
			sql_cur.execute(sql_query)
	sql_con.close()
	return False


def updateToday(db_id, db_pwd, db_db, list_kospi200):
	sql_con = pymysql.connect(host = CONST_HOST, user = db_id, password = db_pwd, db = db_db, charset = CONST_CHARSET)
	sql_cur = sql_con.cursor()
	sql_query = "insert into date_today values('"+getToday()+"')"
	sql_cur.execute(sql_query)
	sql_con.commit()
	
	for item_kospi200 in list_kospi200:
		sql_query = "insert into list_kospi200 values("+item_kospi200[0]+",'"+item_kospi200[1].decode('euc-kr')+"')"
		try:
			sql_cur.execute(sql_query)
		except pymysql.err.ProgrammingError as e:
			if(str(e).find("doesn't exist") >= 0):	
				sql_query = "create table list_kospi200(int_code int, str_name varchar(40), primary key(int_code)) default charset="+CONST_CHARSET
				sql_cur.execute(sql_query)
				sql_con.commit()
				sql_query = "insert into list_kospi200 values("+item_kospi200[0]+",'"+item_kospi200[1].decode('euc-kr')+"')"
				sql_cur.execute(sql_query)
	sql_con.commit()
	sql_con.close()