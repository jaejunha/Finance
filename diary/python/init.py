import os
import requests
import re

from datetime import date

URL_FINANCE = "https://finance.naver.com"
URL_SUM = URL_FINANCE + "/sise/sise_market_sum.nhn"
URL_SUM_SET = URL_FINANCE + "/sise/field_submit.nhn?menu=market_sum&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn"

CONST_KOSPI = 0
CONST_KOSDAQ = 1

def removeNohup():
    if os.path.isfile("nohup.out"):
        os.remove("nohup.out")

def getPort():
    file = open("port.csv", "r")
    int_port = int(file.readlines()[0].strip())
    file.close()

    return int_port

def getAccount(dic_account):
    file = open("account.csv", "r")
    for str_line in file.readlines():
        if len(str_line.strip()) > 0:
            list_ele = str_line.split(",")
            str_id = list_ele[0].strip()
            str_pwd = list_ele[1].strip()
            int_ath = int(list_ele[2].strip())
            dic_account[str_id] = {"pwd": str_pwd, "ath": int_ath}

            if os.path.isdir("data/%s" % str_id) is False:
                os.chdir("data")
                os.mkdir(str_id)
                os.chdir("..")

def getLastPage(int_sosok):
    str_url = "%s?sosok=%d" % (URL_SUM, int_sosok)
	
    str_res = requests.get(str_url)
    list_line = str_res.text.split("\n")
    for str_line in list_line:
        if "맨뒤" in str_line:
            return int(re.findall("\d\d", str_line)[0])

def getHTML(int_sosok, int_page):
    str_url = "%s?sosok=%d%%26page%%3D%d" % (URL_SUM_SET, int_sosok, int_page)
    str_url += "&fieldIds=market_sum"
    str_url += "&fieldIds=debt_total"
    str_url += "&fieldIds=operating_profit"
    str_url += "&fieldIds=per"
    str_url += "&fieldIds=roe"
    str_url += "&fieldIds=pbr"

    str_res = requests.get(str_url)
    return str_res.text.split("\t")

def getItems(list_item, list_line):
    len_line = len(list_line)
    for i in range(len_line):
        if "/item/main.nhn?code=" in list_line[i]:
            str_code = re.findall('=[^"]+', list_line[i])[0][1:]
            str_name = re.findall('">.+</a>', list_line[i])[0][2: -4]

            list_item.append(str_name)

def downloadItem(list_item):
    date_today = date.today()
    str_today = date_today.strftime("%y%m%d")
    try:
        file = open("item.csv", "r")
        list_line = file.readlines()
        if str_today == list_line[0].strip():
            for i, str_line in enumerate(list_line):
                if i == 0:
                    continue

                list_item.append(str_line.strip())
            print("Already item codes are updated")
            return

    except FileNotFoundError:
        pass
       
    file = open("item.csv", "w")
    file.write(str_today + "\n")

    print("Download items")

    for int_page in range(1, getLastPage(CONST_KOSPI) + 1):
        list_line = getHTML(CONST_KOSPI, int_page)
        getItems(list_item, list_line)

    for int_page in range(1, getLastPage(CONST_KOSDAQ) + 1):
        list_line = getHTML(CONST_KOSDAQ, int_page)
        getItems(list_item, list_line)

    for str_item in list_item:
        file.write(str_item + "\n")

    print("Download is finished")


