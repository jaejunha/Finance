import requests
import re
import os

from datetime import datetime

URL_FINANCE = "https://finance.naver.com"
URL_SUM = URL_FINANCE + "/sise/sise_market_sum.nhn"
URL_SUM_SET = URL_FINANCE + "/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn"

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

def getBlackList():
	list_blacklist = []

	try:
		file = open("../_data/blacklist.txt", "r", encoding = "UTF8")
		for line in file.readlines():
			code = line.split(",")[0].strip()
			list_blacklist.append(code)
		file.close()
	except FileNotFoundError:
		pass
	
	return list_blacklist

def getLastPage(sosk):
	url = "%s?sosok=%d" % (URL_SUM, sosk)
	
	res = requests.get(url)
	list_line = res.text.split("\n")
	for line in list_line:
		if "맨뒤" in line:
			return int(re.findall("\d\d", line)[0])

def getHTML(sosok, page):
	url = "%s?sosok=%d%%26page%%3D%d" % (URL_SUM_SET, sosok, page)
	#%3FfieldIds%3Dmarket_sum%26page%3D5
	url += "&fieldIds=market_sum"
	url += "&fieldIds=debt_total"
	url += "&fieldIds=operating_profit"
	url += "&fieldIds=per"
	url += "&fieldIds=roe"
	url += "&fieldIds=pbr"

	res = requests.get(url)
	return res.text.split("\t")

def saveData(file, list_line):
	for i, line in enumerate(list_line):
		if "/item/main.nhn?code=" in list_line[i]:
			code = re.findall('=[^"]+', list_line[i])[0][1:]
			name = re.findall('">.+</a>', list_line[i])[0][2: -4]

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
			if code in list_blacklist:
				continue
			file.write("%s, %s, %d, %d, %d, %f, %f, %f\n" % (code, name, sum, dept, profit, per, roe, pbr))
			print(code, name, sum, dept, profit, per, roe, pbr)

if __name__ == "__main__":

	str_date = datetime.today().strftime("%Y%m%d")

	if os.path.exists("../_data/" + str_date + ".txt") is False:
	
		list_blacklist = getBlackList()

		file_day = open("../_data/" + str_date + ".txt", "w")
		file_day.write("code, name, sum, dept, profit, per, roe, pbr\n")

		for page in range(1, getLastPage(CONST_KOSPI) + 1):
			list_line = getHTML(CONST_KOSPI, page)
			saveData(file_day, list_line)

		for page in range(1, getLastPage(CONST_KOSDAQ) + 1):
			list_line = getHTML(CONST_KOSDAQ, page)
			saveData(file_day, list_line)		
		file_day.close()

	file = open("temp.csv", "w")
	file.write("이름, 시총, 영업이익\n")

	list_sum = []
	list_profit = []
	file_day = open("../_data/" + str_date + ".txt", "r")
	for i, line in enumerate(file_day.readlines()):
		if i == 0:
			continue
		list_line = line.split(",")
		code = list_line[0].strip()
		name = list_line[1].strip()
		sum = int(list_line[2].strip())
		profit = int(list_line[4].strip())

		list_sum.append( (sum, code) )
		list_profit.append( (profit, code) )

		# 적자 제외
		if profit >= 0:
			file.write("%s, %d, %d\n" % (name, sum, profit) )

	list_sum.sort(reverse = True)
	list_profit.sort(reverse = True)
		
	