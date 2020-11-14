import requests
import re

from datetime import datetime

URL_FINANCE = "https://finance.naver.com"
URL_SUM = URL_FINANCE + "/sise/sise_market_sum.nhn"
URL_SUM_SET = URL_FINANCE + "/sise/field_submit.nhn?menu=market_sum&returnUrl=" + URL_SUM

CONST_KOSPI = 0
CONST_KOSDAQ = 1

VAL_GARBAGE = -999999999

NUM_CNT = 10
CONST_SUM = 5
CONST_DEPT = 6
CONST_PROFIT = 7
CONST_PER = 8
CONST_ROE = 9
CONST_PBR = 10

def getLastPage(sosk):
	url = "%s?sosok=%d" % (URL_SUM, sosk)
	
	res = requests.get(url)
	list_line = res.text.split("\n")
	for line in list_line:
		if "맨뒤" in line:
			return int(re.findall("\d\d", line)[0])

def getHTML(sosok, page):
	url = "%s?sosok=%d&page=%d" % (URL_SUM_SET, sosok, page)
	url += "&fieldIds=market_sum"
	url += "&fieldIds=debt_total"
	url += "&fieldIds=operating_profit"
	url += "&fieldIds=per"
	url += "&fieldIds=roe"
	url += "&fieldIds=pbr"

	res = requests.get(url)
	return res.text.split("\t")

if __name__ == "__main__":
	#print(getLastPage(CONST_KOSPI))
	#print(getLastPage(CONST_KOSDAQ))
	
	try:
		file_blacklist = open("../_data/blacklist.txt", "r")
	except FileNotFoundError:
		pass

	file_day = open("../_data/" + datetime.today().strftime("%Y%m%d") + ".txt", "w")

	list_line = getHTML(CONST_KOSPI, 1)
	for i, line in enumerate(list_line):
		if "/item/main.nhn?code=" in list_line[i]:
			code = re.findall('=[^"]+', list_line[i])[0][1:]
			name = re.findall('">.+</a>', list_line[i])[0][2: -4]
			sum = None
			dept = None
			profit = None
			per = None
			roe = None
			pbr = None

			cnt_num = 0
			while cnt_num < NUM_CNT:
				i += 1
				if "number" in list_line[i]:
					cnt_num += 1
					if cnt_num < CONST_SUM:
						continue
					
					res = re.findall(">[-\d.,]+<", list_line[i])
					if cnt_num == CONST_SUM:
						if res:
							sum = int(res[0][1:-1].replace(",", ""))
						else:
							sum = VAL_GARBAGE
					elif cnt_num == CONST_DEPT:
						if res:
							dept = int(res[0][1:-1].replace(",", ""))
						else:
							dept = VAL_GARBAGE
					elif cnt_num == CONST_PROFIT:
						if res:
							profit = int(res[0][1:-1].replace(",", ""))
						else:
							profit = VAL_GARBAGE
					elif cnt_num == CONST_PER:
						if res:
							per = float(res[0][1:-1].replace(",", ""))
						else:
							per = VAL_GARBAGE
					elif cnt_num == CONST_ROE:
						if res:
							roe = float(res[0][1:-1].replace(",", ""))
						else:
							roe = VAL_GARBAGE
					elif cnt_num == CONST_PBR:
						if res:
							pbr = float(res[0][1:-1].replace(",", ""))
						else:
							pbr = VAL_GARBAGE
			print(code, name, sum, dept, profit, per, roe, pbr)
		