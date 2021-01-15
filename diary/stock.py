import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

CONST_8KB = 8192

list_visit = []
list_account = []

def writeObject(res):
	file = open(res.path, "rb")
	data = file.read(CONST_8KB)
	res.wfile.write(data)

	while data:
		data = file.read(CONST_8KB)
		res.wfile.write(data)

	file.close()
				
def writeHTML(res):
    list_date = []
    file = open(res.path, "r", encoding = "utf-8")
    for line in file.readlines():
        if line.strip().startswith(":)") and line.strip().endswith("&") :
            start = line.find(":)")
            end = line.find("&")

            content = "<div>"
            sum_profit = 0
            sum_percent = 0
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
            content += "<td>날짜</td><td>이름</td><td>매수타점(상승일대비)</td><td>매수타점(연속하락)</td><td>수익률</td><td>비고</td>"
            content += "<tr>"
            for i, line_i in enumerate(list_file_line):
                if i == len_file_line - 1:
                    continue
                content += "<tr>"
                list_line_i = line_i.split(",")
                date = int(list_line_i[0].strip())
                list_date.append(date)
                name = list_line_i[1].strip()
                amount = int(list_line_i[6].strip())
                profit = int(list_line_i[7].strip())
                buy_percent = 100 * (float(list_line_i[4].strip()) - float(list_line_i[2].strip())) / float(list_line_i[2])
                buy_count = int(list_line_i[3].strip())
                etc = list_line_i[8].strip()
                content += "<td>%s</td><td>%s</td><td>%.2f%%</td><td>%d</td><td>%+.2f%%</td><td>%s</td>" % (date, name, buy_percent, buy_count, float(profit) / amount * 100, etc)
                
                sum_profit += profit
                sum_percent += buy_percent
                sum_count += buy_count
                total += 1
                if profit > 0:
                    win += 1
                content += "</tr>"
            content += "</table>"
            content += "<br>"
            content += "평균 매수타점 상승일대비 %+.2f%% 연속 %d일 하락<br>" % (sum_percent / len_file_line, sum_count / len_file_line)
            content += "<br>"
            content += "승률 %.2f%% ( %d 승 / %d 전 )<br>" % (win / total * 100, win, total)
            content += "총 실현손익 %s<br>" % format(sum_profit, ",")
            content += "</div>"
            content += "<br>"

            content += "<script>"
            key = None
            kdx = 0
            for date in list_date:
                if key == date:
                    continue
                else:
                    key = date
                    content += "arr_date[%d] = new Array();" % kdx
                    idx = 0
                    for file in sorted(os.listdir("record")):
                        if file.startswith(str(key)):
                            content += "arr_date[%d][%d] = '%s';" % (kdx, idx, file)
                            idx += 1
                    kdx += 1
            content += "</script>"

            content += "<select id='date' onchange='change()'>"
            key = None
            for date in list_date:
                if key == date:
                    continue
                else:
                    key = date
                    content += "<option value='%d'>%d</option>" % (key, key)
            content += "</select>"
            content += "<br>"
            content += "<div id='record'></div>"
            content += "<script> function change(){"
            content += "var idx = $('#date option').index($('#date option:selected'));"
            content += "var str = '';"
            content += "for (var i = 0; i < arr_date[idx].length; ++i){"
            content += "str += '<img width=\"300px\" src=\"record/' + arr_date[idx][i] + '\"/>';}"
            content += "$('#record').html(str);"
            content += "}change();</script>"



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
            if (list_account[0][0] == list_input[0].split("=")[1]) and (list_account[0][1] == list_input[1].split("=")[1]):
                self._redirect("home")
                list_visit.append(self.client_address[0])
            else:
                self._redirect("/")
    def do_GET(self):
        print(self.path)

        access = False
        if self.path == "/":
            access = True
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

if __name__ == "__main__":	

    port = 7777 

    file = open("account.csv", "r")
    for line in file.readlines():
        if len(line.strip()) > 0:
            id = line.split(",")[0].strip()
            pwd = line.split(",")[1].strip()
            list_account.append( (id, pwd) )


    server_http = HTTPServer(("", port), HandlerHTTP)
    server_http.serve_forever()