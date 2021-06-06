import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote

WEB_FINANCE = "https://finance.naver.com"
WEB_FALL = "/sise/field_submit.nhn?menu=fall"
WEB_RET = "&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_fall.nhn%3Fsosok%3D"
WEB_ETC = "&fieldIds=quant&fieldIds=amount&fieldIds=open_val&fieldIds=low_val"

TOTAL_TYPE = 2

IDX_PRICE = 1
IDX_PERCENT = 3
IDX_VOL = 5
IDX_LOW = 7

TOTAL_TOP = 10

str_print = None

def getDicItem(dic_item):
    for int_type in range(TOTAL_TYPE):  
        res = requests.get(WEB_FINANCE + WEB_FALL + WEB_RET + str(int_type) + WEB_ETC)

        list_text = res.text.split("\n")
        bool_find = False
        for int_i, str_line in enumerate(list_text):
            if "/item/main.nhn?code=" in str_line:
                str_code = str_line.split("=")[2].split('"')[0]
                str_name = str_line.split(">")[2].split("<")[0]
                int_number = 0
                bool_find = True
            elif bool_find:
                if 'class="number"' in str_line:
                    int_number += 1
                    if int_number == IDX_PRICE:
                        int_price = int(str_line.split(">")[1].split("<")[0].replace(",", ""))
                    elif int_number == IDX_PERCENT:
                        float_percent = float(list_text[int_i + 2].strip()[:-1])
                    elif int_number == IDX_VOL:
                        int_vol = int(str_line.split(">")[1].split("<")[0].replace(",", ""))
                    elif int_number == IDX_LOW:
                        int_low = int(str_line.split(">")[1].split("<")[0].replace(",", ""))
                        dic_item[str_code] = {"name": str_name, "price": int_price, "percent": float_percent, "vol": int_vol, "low": int_low}
                        bool_find = False
        
def printDicDiff(dic_pre, dic_cur):
    list_diff = []
    
    for str_code in dic_cur.keys():
        if str_code in dic_pre.keys() and dic_cur[str_code]["percent"] <= dic_pre[str_code]["percent"]:
            list_diff.append( (dic_pre[str_code]["percent"] - dic_cur[str_code]["percent"], str_code) )
            
    list_diff.sort(reverse = True)
    
    global str_print
    
    str_print = ""
    for int_i, ele_diff in enumerate(list_diff):
        if int_i == TOTAL_TOP:
            break
        
        float_diff = ele_diff[0]
        str_code = ele_diff[1]
        
        str_print += (dic_cur[str_code]["name"] + ", " + str(dic_cur[str_code]["vol"]) + ", " + str(dic_cur[str_code]["price"]) + "(" + str(dic_cur[str_code]["low"]) + ")" + str(dic_cur[str_code]["percent"]) + "(" + str(float_diff) + "%)<br>")
        print(str_code, float_diff, dic_cur[str_code])
     
def copyDic(dic_pre, dic_cur):
    dic_pre.clear()
    
    for str_code in dic_cur.keys():
        dic_pre[str_code] = {"name": dic_cur[str_code]["name"], "price": dic_cur[str_code]["price"], "percent": dic_cur[str_code]["percent"], "vol": dic_cur[str_code]["vol"], "low": dic_cur[str_code]["low"]}

def updateData():
    dic_pre = {}
    getDicItem(dic_pre)
    dic_cur = {}
    while True:
        getDicItem(dic_cur)
        printDicDiff(dic_pre, dic_cur)
        copyDic(dic_pre, dic_cur)
    
        time.sleep(10)
 
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
        self._set_headers(200)
        self.wfile.write(str_print.encode("euc-kr"))

if __name__ == "__main__":
        thread_crawler = threading.Thread(target = updateData)
        thread_crawler.daemon = True
        thread_crawler.start()	
        
        server_http = HTTPServer(("", 810), HandlerHTTP)
        server_http.serve_forever()