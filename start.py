import urllib2
import random
import os

CONST_KOSPI200 = 'https://finance.naver.com/sise/entryJongmok.nhn?&page='
l_clear = lambda: os.system('cls')
def printMenu():
	print 
	print 'Finance Management Program'
	print '======================================='
	print '1. Random KOSPI 200'
	print '2. Exit'
	print '======================================='

list_kospi200 = []

while True:
	l_clear()
	printMenu()
	str_menu = raw_input('Please select the MENU >> ')
	if str_menu == '1':
		for i in range(1,22):
			str_query = urllib2.urlopen(CONST_KOSPI200 + str(i)).read().split('\n')
			for str_line in str_query:
				if str_line.find('"ctg"')>=0:
					list_kospi200.append((str_line.split('code=')[1].split('"')[0],str_line.split('>')[2].split('<')[0]))
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