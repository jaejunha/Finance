import urllib
import requests
import re
import os
import sys

from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer

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

list_sum = []
list_dept = []
list_profit = []
list_per_p = []
list_per_m = []
list_roe = []
list_pbr_p = []
list_pbr_m = []
dic_item = {}

class myHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		url = urllib.parse.unquote(self.path)
		if "/" in url:
			url = url[1:]
	
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		if url in dic_item.keys():
			for i, ele in enumerate(list_sum):
				if ele[1] == url:
					rank_sum = i + 1
			for i, ele in enumerate(list_dept):
				if ele[1] == url:
					rank_dept = i + 1
			for i, ele in enumerate(list_profit):
				if ele[1] == url:
					rank_profit = i + 1
			for i, ele in enumerate(list_per):
				if ele[1] == url:
					rank_per = i + 1
			for i, ele in enumerate(list_roe):
				if ele[1] == url:
					rank_roe = i + 1
			for i, ele in enumerate(list_pbr):
				if ele[1] == url:
					rank_pbr = i + 1

			self.wfile.write(('<h1 style="color:red;">하지만 지금 지수 높아서 매수는 자제</h1>').encode("euc-kr"))
			self.wfile.write(("<h2>" + url + "</h2>").encode("euc-kr"))
			self.wfile.write("<table>".encode("euc-kr"))

			str = "시가총액\t%s 억원 (%d위, 상위 %.2f%%)<br>" % (format(dic_item[url]["sum"], ","), rank_sum, (rank_sum / len_total) * 100)

			self.wfile.write("<tr>".encode("euc-kr"))
			self.wfile.write(str.encode("euc-kr"))
			self.wfile.write("</tr>".encode("euc-kr"))

			if rank_sum > rank_profit:
				self.wfile.write("<td>".encode("euc-kr"))
				str = "영업이익\t%s 억원 (%d위, 상위 %.2f%%) [시가총액 %d위: %s]<br>" % (format(dic_item[url]["profit"], ","), rank_profit, (rank_profit / len_total) * 100, rank_profit, list_sum[rank_profit - 1][1])
				self.wfile.write(str.encode("euc-kr"))
				self.wfile.write("</td>".encode("euc-kr"))
			else:
				str = "영업이익\t%s 억원 (%d위, 상위 %.2f%%)<br>" % (format(dic_item[url]["profit"], ","), rank_profit, (rank_profit / len_total) * 100)

			self.wfile.write("<tr>".encode("euc-kr"))
			self.wfile.write(str.encode("euc-kr"))
			self.wfile.write("</tr>".encode("euc-kr"))

			if rank_sum > rank_roe:
				str = "ROE\t\t%f (%d위, 상위 %.2f%%) [시가총액 %d위: %s]<br>" % (dic_item[url]["roe"], rank_roe, (rank_roe / len_total) * 100, rank_roe, list_sum[rank_roe - 1][1])
			else:
				str = "ROE\t\t%f (%d위, 상위 %.2f%%)<br>" % (dic_item[url]["roe"], rank_roe,(rank_roe / len_total) * 100)

			self.wfile.write("<tr>".encode("euc-kr"))
			self.wfile.write(str.encode("euc-kr"))
			self.wfile.write("</tr>".encode("euc-kr"))
			
			if rank_sum > rank_per:
				str = "PER\t\t%f (%d위, 상위 %.2f%%) [시가총액 %d위: %s]<br>" % (dic_item[url]["per"], rank_per, (rank_per / len_total) * 100, rank_per, list_sum[rank_per - 1][1])
			else:
				str = "PER\t\t%f (%d위, 상위 %.2f%%)<br>" % (dic_item[url]["per"], rank_per, (rank_per / len_total) * 100)

			self.wfile.write("<tr>".encode("euc-kr"))
			self.wfile.write(str.encode("euc-kr"))
			self.wfile.write("</tr>".encode("euc-kr"))

			if rank_sum > rank_pbr:
				str = "PBR\t\t%f (%d위, 상위 %.2f%%) [시가총액 %d위: %s]<br>" % (dic_item[url]["pbr"], rank_pbr, (rank_pbr / len_total) * 100, rank_pbr, list_sum[rank_pbr - 1][1])
			else:
				str = "PBR\t\t%f (%d위, 상위 %.2f%%)<br>" % (dic_item[url]["pbr"], rank_pbr, (rank_pbr / len_total) * 100)

			self.wfile.write("<tr>".encode("euc-kr"))
			self.wfile.write(str.encode("euc-kr"))
			self.wfile.write("</tr>".encode("euc-kr"))

			str = "부채총액\t%s 억원 (%d위, 상위 %.2f%%) [은행/증권은 특성상 부채가 높음]<br>" % (format(dic_item[url]["dept"], ","), rank_dept, (rank_dept / len_total) * 100)

			self.wfile.write("<tr>".encode("euc-kr"))
			self.wfile.write(str.encode("euc-kr"))
			self.wfile.write("</tr>".encode("euc-kr"))
			self.wfile.write("</table>".encode("euc-kr"))
		return

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

	# Download data (yesterday)
	date_yesterday = datetime.today() - timedelta(days = 1)
	str_date = date_yesterday.strftime("%Y%m%d")
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


	global list_sum, list_dept, list_profit, list_per_p, list_per_m, list_roe, list_pbr_p, list_pbr_m, dic_item
	file_day = open("../_data/" + str_date + ".txt", "r")
	for i, line in enumerate(file_day.readlines()):
		if i == 0:
			continue
		list_line = line.split(",")
		code = list_line[0].strip()
		name = list_line[1].strip()
		sum = int(list_line[2].strip())
		dept = int(list_line[3].strip())
		profit = int(list_line[4].strip())
		per = float(list_line[5].strip())
		roe = float(list_line[6].strip())
		pbr = float(list_line[7].strip())

		list_sum.append( (sum, name) )
		list_dept.append( (dept, name) )
		list_profit.append( (profit, name) )
		list_roe.append( (roe, name) )

		if per >= 0:
			list_per_p.append( (per, name) )
		else:
			list_per_m.append( (per, name) )
		if pbr >= 0:
			list_pbr_p.append( (pbr, name) )
		else:
			list_pbr_m.append( (pbr, name) )

		dic = {"sum": sum, "dept": dept, "profit": profit, "per": per, "roe": roe, "pbr": pbr}
		dic_item[name] = dic

	len_total = len(list_sum)
	list_sum.sort(reverse = True)
	list_dept.sort(reverse = True)
	list_profit.sort(reverse = True)
	list_roe.sort(reverse = True)
	list_per_p.sort()
	list_per_m.sort(reverse = True)
	list_pbr_p.sort()
	list_pbr_m.sort(reverse = True)
	list_per = list_per_p + list_per_m
	list_pbr = list_pbr_p + list_pbr_m

	print("Server is run on port 8080")
	httpd = HTTPServer(("", 8080), myHandler)
	httpd.serve_forever()
