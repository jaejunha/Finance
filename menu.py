import random

import http as HTTP
import dbms as DBMS

def randomKOSPI200(db_id, db_pwd, db_db, bool_update, list_kospi200):
	if DBMS.checkToday(db_id, db_pwd, db_db) == False:
		print 'updating data...'
		list_kospi200 = HTTP.getKOSPI200(db_id, db_pwd, db_db)
	elif bool_update == False:
		list_kospi200 = DBMS.getKOSPI200(db_id, db_pwd, db_db)
	bool_update = True

	while True:
		str_answer = raw_input('Would you want to see the list of KOSPI 200?(yes/no) >> ')
		if str_answer == 'yes' or str_answer == 'YES':
			int_i = 1
			for item_kospi200 in list_kospi200:
				print str(int_i) + '. ' +item_kospi200[0] + ' ' + item_kospi200[1]
				int_i += 1
			break
		elif str_answer == 'no' or str_answer == 'NO':
			break
		else:
			print 'Check your input'

	int_size = len(list_kospi200)
	list_random = []
	int_random = 5

	while True:
		str_answer = raw_input('How many you want to choose? >> ')
		try:
			int_random = int(str_answer)
			if int_random >= 1 and int_random <= 200:
				break
			else:
				print 'check your input'
		except Exception as e:
			print 'Check your input'
	while len(list_random) < int_random:
		item_kospi200 = list_kospi200[random.randrange(0, int_size + 1)]
		if item_kospi200 in list_random:
			pass
		else:
			list_random.append(item_kospi200)
	int_i = 1
	for item_random in list_random:
		print str(int_i) + '. ' +item_random[0] + ' ' + item_random[1]
		int_i += 1
	str_answer = raw_input('Please Enter the any key')

	return bool_update, list_kospi200