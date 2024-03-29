import requests
import time
import threading
import os
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

TOTAL_TOP = 15

str_print = None

def getDicTotal(dic_total):
    list_name = os.listdir()
    list_candidate = []
    for str_name in list_name:
        if ".csv" in str_name:
            list_candidate.append( (int(str_name.replace(".csv", "")), str_name) )
            
    list_candidate.sort(reverse = True)
    file = open(list_candidate[0][1], "r")
    for int_i, str_line in enumerate(file.readlines()):
        if int_i == 0:
            continue
            
        list_ele = str_line.split(",")
        str_code = list_ele[0].strip()
        int_day = int(list_ele[1].strip())
        float_total = float(list_ele[4].strip()[:-1])
        
        dic_total[str_code] = {"day": int_day, "total": float_total}

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
        
def printDic(dic_total, dic_pre, dic_cur):
    list_rate = []
    list_total = []
    list_diff = []
    
    for str_code in dic_cur.keys():
        list_rate.append( (dic_cur[str_code]["percent"], str_code) )
        
        if str_code in dic_total.keys():
            float_total = ((1 + dic_total[str_code]["total"] / 100.0)*(1 + dic_cur[str_code]["percent"] / 100.0) - 1) * 100
            list_total.append( (float_total, str_code) )
        else:
            list_total.append( (dic_cur[str_code]["percent"], str_code) )
            
        if str_code in dic_pre.keys() and dic_cur[str_code]["percent"] <= dic_pre[str_code]["percent"]:
            list_diff.append( (dic_pre[str_code]["percent"] - dic_cur[str_code]["percent"], str_code) )
    
    list_rate.sort()
    list_total.sort()
    list_diff.sort(reverse = True)
    
    global str_print
    
    str_print = "<h1>등락률</h1>"
    str_print += "<table style='width: 100%;'>"
    str_print += "<tr>"
    str_print += "<td>이름</td><td>등락률</td><td>거래대금</td><td>현재가 (저가)</td>"
    str_print += "</tr>"
    for int_i, ele_total in enumerate(list_rate):
        if int_i == TOTAL_TOP:
            break
        
        str_code = ele_total[1]
        
        str_print += "<tr>"
        str_print += "<td>%s</td>" % dic_cur[str_code]["name"]
        str_print += "<td>%.2f%%</td>" % dic_cur[str_code]["percent"]
        str_print += "<td>%s</td>" % dic_cur[str_code]["vol"]
        str_print += "<td>%s (%s)</td>" % (format(dic_cur[str_code]["price"], ","), format(dic_cur[str_code]["low"], ","))
        str_print += "</tr>"
    str_print += "</table>"
    
    str_print += "<h1>누적등락률</h1>"
    str_print += "<table style='width: 100%;'>"
    str_print += "<tr>"
    str_print += "<td>이름</td><td>등락률 (누적)</td><td>하락 일수</td><td>거래대금</td><td>현재가 (저가)</td>"
    str_print += "</tr>"
    for int_i, ele_total in enumerate(list_total):
        if int_i == TOTAL_TOP:
            break
        
        float_total = ele_total[0]
        str_code = ele_total[1]
        
        str_print += "<tr>"
        str_print += "<td>%s</td>" % dic_cur[str_code]["name"]
        str_print += "<td>%.2f%% (%.2f%%)</td>" % (dic_cur[str_code]["percent"], float_total)
        if str_code in dic_total.keys():
            str_print += "<td>%d</td>" % (dic_total[str_code]["day"] + 1)
        else:
            str_print += "<td>1</td>"
        str_print += "<td>%s</td>" % dic_cur[str_code]["vol"]
        str_print += "<td>%s (%s)</td>" % (format(dic_cur[str_code]["price"], ","), format(dic_cur[str_code]["low"], ","))
        str_print += "</tr>"
    str_print += "</table>"
    
    str_print += "<h1>변화량</h1>"
    str_print += "<table style='width: 100%;'>"
    str_print += "<tr>"
    str_print += "<td>이름</td><td>등락률 (직전 차이)</td><td>거래대금</td><td>현재가 (저가)</td>"
    str_print += "</tr>"
    for int_i, ele_diff in enumerate(list_diff):
        if int_i == TOTAL_TOP:
            break
        
        float_diff = ele_diff[0]
        str_code = ele_diff[1]
        
        str_print += "<tr>"
        str_print += "<td>%s</td>" % dic_cur[str_code]["name"]
        str_print += "<td>%.2f%% (%.2f%%)</td>" % (dic_cur[str_code]["percent"], float_diff)
        str_print += "<td>%s</td>" % dic_cur[str_code]["vol"]
        str_print += "<td>%s (%s)</td>" % (format(dic_cur[str_code]["price"], ","), format(dic_cur[str_code]["low"], ","))
        str_print += "</tr>"
        print(str_code, float_diff, dic_cur[str_code])
    str_print += "</table>"
     
def copyDic(dic_pre, dic_cur):
    dic_pre.clear()
    
    for str_code in dic_cur.keys():
        dic_pre[str_code] = {"name": dic_cur[str_code]["name"], "price": dic_cur[str_code]["price"], "percent": dic_cur[str_code]["percent"], "vol": dic_cur[str_code]["vol"], "low": dic_cur[str_code]["low"]}

def updateData():
    
    dic_total = {}
    getDicTotal(dic_total)

    dic_pre = {}
    getDicItem(dic_pre)
    dic_cur = {}
    while True:
        getDicItem(dic_cur)
        printDic(dic_total, dic_pre, dic_cur)
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