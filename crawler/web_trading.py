# -*- coding: UTF-8 -*-
import requests
import time
import threading
import os
import collector
import finder
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote

WEB_PORT = 810

CONST_1H = 3600
CONST_8KB = 8192

TIME_PM_6 = 18

str_print = None

def updateData():
    while True:
        now = time.localtime()
        if now.tm_hour >= TIME_PM_6:
            collector.downloadFile()
        time.sleep(CONST_1H)
 
class HandlerHTTP(BaseHTTPRequestHandler):
    def setup(self):
        BaseHTTPRequestHandler.setup(self)
        self.request.settimeout(2)

    def _set_headers(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
	
    def _redirect(self, url):
        self.send_response(302)
        self.send_header("Location", url)
        self.end_headers()
		
    def do_GET(self):
        str_print = ""
        
        if ".csv" in self.path:
            str_path = self.path[1:]
            if os.path.isfile(str_path):
                self._set_headers(200)
                file = open(str_path, "rb")
                data = file.read(CONST_8KB)
                self.wfile.write(data)

                while data:
                    data = file.read(CONST_8KB)
                    self.wfile.write(data)

                file.close()
            else:
                self._redirect("/")

        elif self.path == "/data.zip":
            if os.path.isdir("data"):
                self._set_headers(200)

                os.system("cp -rf data dataall")
                os.system("zip data.zip dataall/*")

                file = open("data.zip", "rb")
                data = file.read(CONST_8KB)
                self.wfile.write(data)

                while data:
                    data = file.read(CONST_8KB)
                    self.wfile.write(data)

                file.close()

                os.system("rm -rf dataall")
                os.system("rm data.zip")
            else:
                self._redirect("/")
 
        elif self.path == "/":
            self._set_headers(200)

            str_print += '<head>'
            str_print += '<style>'
            str_print += 'a {text-decoration: none; color: #fff;}'
            str_print += '</style>'
            str_print += '</head>'
            str_print += '<body style="margin: 0;">'
            str_print += '<div style="background: #aaf; color: #fff; height: 40px; text-align: center; line-height: 40px; vertical-align: center;">'
            str_print += '<a href="download">Download</a>'
            str_print += '&nbsp;|&nbsp;'
            str_print += '(Developing...)'
            str_print += '</div>'
            str_print += '<br>'

            float_rate = 3
            """
            str_recent, list_fluctuation = finder.getFluctuation(False, True, float_rate)
            str_print += '<h1>%s 기준</h1>' % str_recent 
            str_print += '<h3>시가대비 변동성 %d%% 이상 중 상승종목</h3>' % float_rate
            for ele_fluctuation in list_fluctuation:
                str_print += (ele_fluctuation[1] + "<br>")
            """
            str_recent, str_fluctuation = finder.getFluctuation(True, False, float_rate)
            str_print += '<h1>%s 기준</h1>' % str_recent 
            str_print += '<h3>시가대비 변동성 %d%% 이상 중 하락종목</h3>' % float_rate

            str_print += str_fluctuation

            str_print += '</body>'

            self.wfile.write(str_print.encode("euc-kr"))

        elif self.path == "/download":
            self._set_headers(200)
            
            try:
                list_data = os.listdir("data")
                list_data.sort(reverse = True)
                str_print += '<a href="data.zip" download="data.zip">일괄 다운로드</a><br>'
                for str_data in list_data:
                    int_data = int(str_data.split(".")[0])
                    int_year = int_data / 10000
                    int_month = (int_data % 10000) / 100
                    int_day = int_data % 100
                    str_print += '<a href="data/%s" download="%s">%04d년 %02d월 %02d일</a><br>' % (str_data, str_data, int_year, int_month, int_day)
            except Exception as e:
                print(e)
                pass
            self.wfile.write(str_print.encode("euc-kr"))
        else:
            self._redirect("/")

if __name__ == "__main__":
        
        thread_crawler = threading.Thread(target = updateData)
        thread_crawler.daemon = True
        thread_crawler.start()	
        
        
        server_http = HTTPServer(("", WEB_PORT), HandlerHTTP)
        server_http.serve_forever()
