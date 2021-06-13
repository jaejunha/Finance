# -*- coding: UTF-8 -*-
import requests
import time
import threading
import os
import collector
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote

WEB_PORT = 810

CONST_1H = 3600
CONST_8KB = 8192

str_print = None

def updateData():
    while True:
        now = time.localtime()
        if now.tm_hour >= 18:
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
            str_print = "" 

            try:
                list_data = os.listdir("data")
                list_data.sort(reverse = True)
                str_print += '<a href="data.zip" download="data.zip">일괄 다운로드</a><br>'
                for str_data in list_data:
                    str_print += '<a href="data/%s" download="%s">%s</a><br>' % (str_data, str_data, str_data)
            except:
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
