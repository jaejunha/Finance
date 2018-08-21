import random

import util as UTIL
import dbms as DBMS
import http as HTTP

if __name__ == '__main__':
	db_id, db_pwd, db_db, error = DBMS.checkDB()

	while error == False:
		UTIL.printMenu()
		str_menu = raw_input('Please select the MENU >> ')
		if str_menu == '1':
			if DBMS.checkToday(db_id, db_pwd, db_db) == False:
				list_kospi200 = HTTP.getKOSPI200()
			str_answer = raw_input('Would you want to see the list of KOSPI 200?(yes/no) >> ')
			if str_answer == 'yes' or str_answer == 'YES':
				int_i = 1
				for item_kospi200 in list_kospi200:
					print str(int_i) + '. ' +item_kospi200[0] + ' ' + item_kospi200[1]
					int_i += 1
			int_size = len(list_kospi200)
			list_random = []
			str_answer = raw_input('How many you want to choose? >> ')
			int_random = int(str_answer)

			#Need to try catch statement(wrong input)
			#Need to try catch statement(out of range)
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
		else:
			print 'Good Bye!'
			break