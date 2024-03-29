import os
import copy
import urllib
from datetime import date
from http.server import HTTPServer, BaseHTTPRequestHandler

CONST_8KB = 8192

list_visit = []
dic_ip = {}

dic_account = None
list_item = None

def makeHandler(dic_account_f, list_item_f):
    global dic_account, list_item
    
    dic_account = copy.deepcopy(dic_account_f)
    list_item = copy.deepcopy(list_item_f)

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
                len_header = int(self.headers['Content-length'])
                utf8 = self.rfile.read(len_header).decode("utf-8")
                utf8_treat = utf8.replace("+", " ")
                list_input = utf8_treat.split("&")
            
                year = int(list_input[0].split("=")[1])
                month = int(list_input[1].split("=")[1])
                day = int(list_input[2].split("=")[1])
                item = urllib.parse.unquote(list_input[3].split("=")[1])
                try:
                    buy = int(list_input[4].split("=")[1])
                except:
                    buy = 0
                try:
                    unit = int(list_input[5].split("=")[1])
                except:
                    unit = 0
           
                if item != "" and unit != 0 and buy != 0:
                    str_id = dic_ip[self.client_address[0]]
                    str_date = "%4d%02d%02d" % (year, month, day)
            
                    file = open("data/%s/%s.csv" % (str_id, str_date), "a")
                    file.write("%s, %d, %d\n" % (item, buy, unit))

                self._redirect("home")

            elif self.path == "/delete":
                len_header = int(self.headers['Content-length'])
                utf8 = self.rfile.read(len_header).decode("utf-8")
                utf8_treat = utf8.replace("+", " ")
                list_input = utf8_treat.split("&")
        
                str_date = list_input[0].split("=")[1]
                str_item = urllib.parse.unquote(list_input[1].split("=")[1])
                str_buy = list_input[2].split("=")[1]
                str_unit = list_input[3].split("=")[1]
                str_except = "%s, %s, %s\n" % (str_item, str_buy, str_unit)

                str_id = dic_ip[self.client_address[0]]
            
                file = open("data/%s/%s.csv" % (str_id, str_date), "r")
                list_line = file.readlines()
                file.close()

                file = open("data/%s/%s.csv" % (str_id, str_date), "w")
                for str_line in list_line:
                    if str_line == str_except:
                        continue
                    file.write(str_line)
                file.close()

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

    return HandlerHTTP

def writeObject(res):
	file = open(res.path, "rb")
	str_data = file.read(CONST_8KB)
	res.wfile.write(str_data)

	while str_data:
		str_data = file.read(CONST_8KB)
		res.wfile.write(str_data)

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
            content += "평균 매수타점 상승일대비 %+.2f%% 연속 %.1f 일 하락<br>" % (sum_buy_percent / len_file_line, sum_count / len_file_line)
            content += "<br>"
            content += "<hr>"
            content += "<br>"
            content += "<table width='100%'>"
            content += "<tr><td>날짜</td><td>실현손익(전에 물린 손절 제외)</td><td>매수타점(상승일대비)</td><td>매수타점(연속하락)</td></tr>"
            for date in dic_day.keys():
                str_profit = format(dic_day[date]["profit"], ",")
                if dic_day[date]["profit"] > 0:
                    str_profit = "+" + str_profit
                content += "<tr><td>%d</td><td>%s</td><td>%.2f%%</td><td>%d</td></tr>" % (date, str_profit, (dic_day[date]["buy_percent"] / dic_day[date]["count"]), (dic_day[date]["buy_count"] / dic_day[date]["count"]))
            content += "</table>"
            content += "<br>"
            content += "총 %d 거래일<br>" % len(dic_day)
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

        if line.strip().startswith(":)codes&"):
            start = line.find(":)")
            end = line.find("&")

            content = ""

            for item in list_item:
                content += '<option value="%s">' % item

            line = line.replace(line[start: end + 1], content)

        if line.strip().startswith(":)items&"):
            start = line.find(":)")
            end = line.find("&")

            content = '<table width="100%">'
            content += "<tr>"
            content += "<td>날짜</td>"
            content += "<td>종목</td>"
            content += "<td>가격</td>"
            content += "<td>수량</td>"
            content += "</tr>"
            id = dic_ip[res.client_address[0]]
            list_file = os.listdir("data/%s" % id)
            list_file.sort()
            for file_name in list_file:
                file = open("data/%s/%s" % (id, file_name), "r")
                for file_line in file.readlines():
                    content += "<tr>"
                    list_line = file_line.split(",")
                    date = file_name.split(".")[0]
                    name = list_line[0].strip()
                    buy = list_line[1].strip()
                    unit = list_line[2].strip()
                    content += "<td>%s</td>" % date
                    content += "<td>%s</td>" % name
                    content += "<td>%s</td>" % buy
                    content += "<td>%s</td>" % unit
                    content += "<td style='text-align:right;'><button onclick='deleteItem(%s, \"%s\", %s, %s)'>삭제</button></td>" % (date, name, buy, unit)
                    content += "</tr>"
            content += "</table>"
            content += "<script>"
            content += "function deleteItem(int_date, str_name, int_buy, int_unit){"
            content += "var form = document.createElement('form');"
            content += "form.setAttribute('method', 'post');"
            content += "form.setAttribute('action', 'delete');"
            content += "document.charset = 'utf-8';"
            content += "var input_date = document.createElement('input');"
            content += "input_date.setAttribute('type', 'hidden');"
            content += "input_date.setAttribute('name', 'date');"
            content += "input_date.setAttribute('value', int_date);"
            content += "form.appendChild(input_date);"
            content += "var input_name = document.createElement('input');"
            content += "input_name.setAttribute('type', 'hidden');"
            content += "input_name.setAttribute('name', 'name');"
            content += "input_name.setAttribute('value', str_name);"
            content += "form.appendChild(input_name);"
            content += "var input_buy = document.createElement('input');"
            content += "input_buy.setAttribute('type', 'hidden');"
            content += "input_buy.setAttribute('name', 'buy');"
            content += "input_buy.setAttribute('value', int_buy);"
            content += "form.appendChild(input_buy);"
            content += "var input_unit = document.createElement('input');"
            content += "input_unit.setAttribute('type', 'hidden');"
            content += "input_unit.setAttribute('name', 'unit');"
            content += "input_unit.setAttribute('value', int_unit);"
            content += "form.appendChild(input_unit);"
            content += "document.body.appendChild(form);"
            content += "form.submit();"
            content += "}"
            content += "</script>"
            line = line.replace(line[start: end + 1], content)


        res.wfile.write(line.encode())

    file.close()

