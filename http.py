import urllib2

CONST_KOSPI200 = 'https://finance.naver.com/sise/entryJongmok.nhn?&page='

def getKOSPI200():
	list_kospi200 = []
	for i in range(1,22):
		str_query = urllib2.urlopen(CONST_KOSPI200 + str(i)).read().split('\n')
		for str_line in str_query:
			if str_line.find('"ctg"')>=0:
				list_kospi200.append((str_line.split('code=')[1].split('"')[0],str_line.split('>')[2].split('<')[0]))
	return list_kospi200