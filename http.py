import urllib2
import re
p = re.compile('.*[0-9]+\.[0-9]*(\%)?.*')

import dbms as DBMS

CONST_LIST_KOSPI200 = 'https://finance.naver.com/sise/entryJongmok.nhn?&page='
CONST_VALUE_KOSPI200 = 'https://finance.naver.com/sise/sise_index.nhn?code=KPI200'

def getListOfKOSPI200(db_id, db_pwd, db_db):
	list_kospi200 = []
	for i in range(1,22):
		str_query = urllib2.urlopen(CONST_LIST_KOSPI200 + str(i)).read().split('\n')
		for str_line in str_query:
			if str_line.find('"ctg"')>=0:
				list_kospi200.append((str_line.split('code=')[1].split('"')[0],str_line.split('>')[2].split('<')[0]))

	DBMS.updateToday(db_id, db_pwd, db_db, list_kospi200)
	return list_kospi200

def printValueOfKOSPI200():
	str_query = urllib2.urlopen(CONST_VALUE_KOSPI200).read().split('\n')
	str_info = 'KOSPI200: '
	str_temp = ''
	bool_table = False
	int_index = 0
	for str_line in str_query:
		if bool_table == True:
			m = p.match(str_line)
			if m:
				if int_index == 0:
					str_info += m.group().split('>')[2].split('<')[0]
				elif int_index == 1:
					str_temp = '('+m.group().strip()+')'
				else:
					str_info += ', '+m.group().strip()+str_temp

				int_index += 1
				if int_index == 3:
					break
			if str_line.find('/table') >= 0:
				bool_table = False
				break
		elif str_line.find('table') >= 0:
			bool_table = True
	print str_info
			
	