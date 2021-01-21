import os
import sys
import requests
import re
from datetime import date
from http.server import HTTPServer, BaseHTTPRequestHandler

URL_FINANCE = "https://finance.naver.com"
URL_SUM = URL_FINANCE + "/sise/sise_market_sum.nhn"
URL_SUM_SET = URL_FINANCE + "/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn"

CONST_KOSPI = 0
CONST_KOSDAQ = 1

CONST_8KB = 8192

list_visit = []
dic_ip = {}
dic_account = {}

list_item = []

def writeObject(res):
	file = open(res.path, "rb")
	data = file.read(CONST_8KB)
	res.wfile.write(data)

	while data:
		data = file.read(CONST_8KB)
		res.wfile.write(data)

	file.close()
				
def writeHTML(res):
    dic_day = {}
    key_date = None
    file = open(res.path, "r", encoding = "utf-8")
    for line in file.readlines():
        if line.strip().startswith(":)statistics&"):
            start = line.find(":)")
            end = line.find("&")

            content = "<div>"
            sum_result = 0
            sum_gain = 0
            sum_loss = 0
            sum_amount_gain = 0
            sum_amount_loss = 0
            sum_buy_percent = 0
            sum_count = 0
            total = 0
            win = 0
            
            file_i = open("data.csv", "r")
            content += "<table width='100%'>"
            list_file_line = file_i.readlines()
            len_file_line = len(list_file_line)
            list_file_line.reverse()
            if list_file_line[0].strip() == "":
                del list_file_line[0]
                len_file_line -= 1
            content += "<tr>"
            content += "<td>날짜</td><td>이름</td><td>매수타점(상승일대비)</td><td>매수타점(연속하락)</td><td>수익률</td><td>전량</td><td>비고</td>"
            content += "<tr>"

            for i, line_i in enumerate(list_file_line):
                if i == len_file_line - 1:
                    continue

                list_line_i = line_i.split(",")
                date = int(list_line_i[0].strip())
                if date != key_date:
                    key_date = date
                    dic_day[date] = {}
                    dic_day[date]["profit"] = 0
                    dic_day[date]["count"] = 0
                    dic_day[date]["buy_percent"] = 0
                    dic_day[date]["buy_count"] = 0
                name = list_line_i[1].strip()
                amount = int(list_line_i[6].strip())
                result = int(list_line_i[7].strip())
                buy_percent = 100 * (float(list_line_i[4].strip()) - float(list_line_i[2].strip())) / float(list_line_i[2])
                buy_count = int(list_line_i[3].strip())
                all = list_line_i[8].strip()
                etc = list_line_i[9].strip()

                if result > 0:
                    content += "<tr style='background:#fcc;'>"
                else:
                    content += "<tr style='background:#ccf;'>"
                content += "<td>%s</td><td>%s</td><td>%.2f%%</td><td>%d</td><td>%+.2f%%</td><td>%s</td><td>%s</td>" % (date, name, buy_percent, buy_count, float(result) / amount * 100, all, etc)
            
                sum_result += result
                dic_day[date]["profit"] += result 
                dic_day[date]["count"] += 1
                dic_day[date]["buy_percent"] += buy_percent
                dic_day[date]["buy_count"] += buy_count
                sum_buy_percent += buy_percent
                sum_count += buy_count
                total += 1
                if result > 0:
                    sum_gain += result
                    sum_amount_gain += amount
                    win += 1
                else:
                    sum_loss += result
                    sum_amount_loss += amount
                content += "</tr>"
            content += "</table>"
            content += "<br>"
            content += "평균 매수타점 상승일대비 %+.2f%% 연속 %d일 하락<br>" % (sum_buy_percent / len_file_line, sum_count / len_file_line)
            content += "<br>"
            content += "<hr>"
            content += "<br>"
            content += "<table width='100%'>"
            content += "<tr><td>날짜</td><td>실현손익(전에 물린 손절 제외)</td><td>매수타점(상승일대비)</td><td>매수타점(연속하락)</td></tr>"
            for date in dic_day.keys():
                content += "<tr><td>%d</td><td>%s</td><td>%.2f%%</td><td>%d</td></tr>" % (date, dic_day[date]["profit"], (dic_day[date]["buy_percent"] / dic_day[date]["count"]), (dic_day[date]["buy_count"] / dic_day[date]["count"]))
            content += "</table>"
            content += "<br>"
            content += "총 실현손익(전에 물린 손절 제외) %s<br>" % format(sum_result, ",")
            content += "<br>"
            content += "<hr>"
            content += "<br>"
            content += "승률 %.2f%% ( %d 승 / %d 전 )<br>" % (win / total * 100, win, total)
            content += "실질 승률 %.2f%%<br>" % (sum_amount_gain / (sum_amount_gain + sum_amount_loss) * 100.0)
            content += "평균 익절(세금 + 수수료 고려) %+.2f%%<br>" % (sum_gain / sum_amount_gain * 100.0)
            content += "평균 손절(세금 + 수수료 고려) %+.2f%%<br>" % (sum_loss / sum_amount_loss * 100.0)
            content += "</div>"
            content += "<br>"

            content += "<script>"
            for i, date in enumerate(dic_day.keys()):
                content += "arr_date[%d] = new Array();" % i
                idx = 0
                for file_name in sorted(os.listdir("record")):
                    if file_name.startswith(str(date)):
                        content += "arr_date[%d][%d] = '%s';" % (i, idx, file_name)
                        idx += 1
            content += "</script>"

            content += "<select id='date' onchange='select()'>"
            for date in dic_day.keys():
                content += "<option value='%d'>%d</option>" % (date, date)
            content += "</select><br>"
            content += "<br>"
            content += "<div id='record'></div>"
            content += "<script> function select(){"
            content += "var idx = $('#date option').index($('#date option:selected'));"
            content += "var str = '';"
            content += "for (var i = 0; i < arr_date[idx].length; ++i){"
            content += "str += '<img width=\"300px\" src=\"record/' + arr_date[idx][i] + '\"/>';}"
            content += "$('#record').html(str);"
            content += "}select();</script>"
            
            line = line.replace(line[start: end + 1], content)

        if line.strip().startswith(":)user&"):
            start = line.find(":)")
            end = line.find("&")

            content = ""

            if dic_account[dic_ip[res.client_address[0]]]["ath"] == 0:
                content += '<hr class="solid">'
                content += '<span onclick="change(1)">dreamline91</span>'
            else:
                for id in dic_account.keys():
                    if dic_account[id]["ath"] == 0:
                        continue
                    else:
                        if dic_account[id]["ath"] == 1:
                            content += '<hr class="solid">'
                        else:
                            content += '<hr class="dash">'
                        content += '<span onclick="change(%d)">%s</span>' % (dic_account[id]["ath"], id)

            line = line.replace(line[start: end + 1], content)

        if line.strip().startswith(":)change&"):
            start = line.find(":)")
            end = line.find("&")

            auth = dic_account[dic_ip[res.client_address[0]]]["ath"]
            if auth == 0:
                content += "change(1);"
            else:
                content = "change(%d);" % auth

            line = line.replace(line[start: end + 1], content)

        if line.strip().startswith(":)items&"):
            start = line.find(":)")
            end = line.find("&")

            content = ""

            for item in list_item:
                content += '<option value="%s">' % item

            line = line.replace(line[start: end + 1], content)

        res.wfile.write(line.encode())

    file.close()

class HandlerHTTP(BaseHTTPRequestHandler):

    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(1)

    def _set_headers(self, code, type = "html"):
        self.send_response(code)
        if type == "html" or type == "css" or type == "js":
            self.send_header('Content-type', 'text/' + type)
        else:
            self.send_header('Content-type', 'image/' + type)
        self.end_headers()
	
    def _redirect(self, url):
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()

    def do_POST(self):
        if self.path == "/check":
            length = int(self.headers['Content-length'])
            raw_input = self.rfile.read(length).decode("utf-8")
            list_input = raw_input.split("&")
            find = False

            for id in dic_account.keys():
                if (id == list_input[0].split("=")[1]) and (dic_account[id]["pwd"] == list_input[1].split("=")[1]):
                    self._redirect("home")
                    list_visit.append(self.client_address[0])
                    dic_ip[self.client_address[0]] = id
                    find = True
                    break
            
            if find == False:
                self._redirect("/")

        elif self.path == "/add":
            self._redirect("home")

    def do_GET(self):
        print(self.path)

        access = False
        if self.path == "/":
            access = True
            self.path = "login.html"
        elif self.path == "/logout":
            access = True

            for i, ip in enumerate(list_visit[:]):
                if ip == self.client_address[0]:
                    del list_visit[i]
                    break

            self.path = "login.html"
        elif self.path == "/home":
            access = True
            if self.client_address[0] in list_visit:
                self.path = "home.html"
            else:
                self.path = "login.html"
        else:
            access = False
            self.path = "." + self.path
        try:
            if (".png" in self.path) or (".jpg" in self.path) or (".gif" in self.path) or (".ico" in self.path) or (".css" in self.path) or (".js" in self.path):
                self._set_headers(200, self.path.split(".")[-1])
                writeObject(self)
	
            else:
                if access is False:
                    raise FileNotFoundError

                self._set_headers(200, "html")
                writeHTML(self)

        except FileNotFoundError:
            self._set_headers(404)
            self.wfile.write(bytes(b"404 Not Found"))		
        except Exception as e:
            print(e)

def getLastPage(sosok):
	url = "%s?sosok=%d" % (URL_SUM, sosok)
	
	res = requests.get(url)
	list_line = res.text.split("\n")
	for line in list_line:
		if "맨뒤" in line:
			return int(re.findall("\d\d", line)[0])

def getHTML(sosok, page):
	url = "%s?sosok=%d%%26page%%3D%d" % (URL_SUM_SET, sosok, page)
	url += "&fieldIds=market_sum"
	url += "&fieldIds=debt_total"
	url += "&fieldIds=operating_profit"
	url += "&fieldIds=per"
	url += "&fieldIds=roe"
	url += "&fieldIds=pbr"

	res = requests.get(url)
	return res.text.split("\t")

def getItems(list_line):
	for i, line in enumerate(list_line):
		if "/item/main.nhn?code=" in list_line[i]:
			code = re.findall('=[^"]+', list_line[i])[0][1:]
			name = re.findall('">.+</a>', list_line[i])[0][2: -4]

			list_item.append(name)


def downloadItem():
    today = date.today()
    str_today = today.strftime("%y%m%d")
    try:
        file = open("item.csv", "r")
        list_line = file.readlines()
        if str_today == list_line[0].strip():
            for i, line in enumerate(list_line):
                if i == 0:
                    continue

                list_item.append(line.strip())
            print("Already item codes are updated")
            return

    except FileNotFoundError:
        pass
       
    file = open("item.csv", "w")
    file.write(str_today + "\n")

    print("Download items")

    for page in range(1, getLastPage(CONST_KOSPI) + 1):
        list_line = getHTML(CONST_KOSPI, page)
        getItems(list_line)

    for page in range(1, getLastPage(CONST_KOSDAQ) + 1):
        list_line = getHTML(CONST_KOSDAQ, page)
        getItems(list_line)

    for item in list_item:
        file.write(item + "\n")

    print("Download is finished")

if __name__ == "__main__":	

    file = open("port.csv", "r")
    port = int(file.readlines()[0].strip())

    file = open("account.csv", "r")
    for line in file.readlines():
        if len(line.strip()) > 0:
            list_line = line.split(",")
            id = list_line[0].strip()
            pwd = list_line[1].strip()
            ath = int(list_line[2].strip())
            dic_account[id] = {"pwd": pwd, "ath": ath}

    downloadItem()

    server_http = HTTPServer(("", port), HandlerHTTP)
    server_http.serve_forever()
