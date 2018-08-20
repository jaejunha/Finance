import pymysql
import json

def connectDB():
	error = False
	file_json = open('db.json','r')
	json_data = json.load(file_json)
	file_json.close()
	try:
		sql_con = pymysql.connect(host='localhost', user=json_data["ID"], password=json_data["PWD"], db=json_data["DB"], charset='utf8')
	except pymysql.err.InternalError as e:
		if str(e).find("Unknown database") >= 0 :
			sql_con = pymysql.connect(host='localhost', user=json_data["ID"], password=json_data["PWD"], charset='utf8')
			sql_cur = sql_con.cursor()
			sql_query = "create database finance"
			sql_cur.execute(sql_query)
			sql_con.commit()
			sql_con.close()
			sql_con = pymysql.connect(host='localhost', user=json_data["ID"], password=json_data["PWD"], db=json_data["DB"], charset='utf8')
		else:
			error = True
	return error