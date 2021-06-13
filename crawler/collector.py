import datetime
import requests
import sys
import os
import filecmp

"""
NAVER로 부터 Data 크롤링
"""
WEB_NAVER = "https://finance.naver.com/"
WEB_SISE_NORMAL = WEB_NAVER + "sise/sise_market_sum.nhn"
WEB_SISE_FIELD = WEB_NAVER + "sise/field_submit.nhn?menu=market_sum"
WEB_SISE_RET = "&returnUrl=http%3A%2F%2Ffinance.naver.com%2Fsise%2Fsise_market_sum.nhn"
WEB_PARA = "&fieldIds=amount&fieldIds=market_sum&fieldIds=open_val&fieldIds=high_val&fieldIds=low_val"

NUM_TYPE = 2
TYPE_KOSPI = 0
TYPE_KOSDAQ = 1

PARSER_CODE = "/item/main.nhn?code="

IDX_CLOSE = 1
IDX_DELTA = 2
IDX_PERCENT = 3
IDX_VOLUME = 5
IDX_OPEN = 6
IDX_HIGH = 7
IDX_LOW = 8
IDX_SUM = 9

"""
코스피 / 코스닥 목록 중 마지막 페이지 구하기
"""
def getLastPage(int_type):
    int_last = None
    res = requests.get("%s?sosok=%d" % (WEB_SISE_NORMAL, int_type))
    for str_line in res.text.split("\n"):
        if "맨뒤" in str_line:
            int_last = int(str_line[str_line.find("page") + 5:].split('"')[0].strip())
            break
    
    if int_last == None:
        print("페이지 오류!, 마지막 페이지 파악이 불가능합니다")
        sys.exit(1)
    
    return int_last

"""
딕셔너리에 종목 정보 저장
"""
def saveItemInfo(dic_item, int_type, int_page):
    res = requests.get("%s%s%%3Fsosok%%3D%d%%26page%%3D%d%s" % (WEB_SISE_FIELD, WEB_SISE_RET, int_type, int_page, WEB_PARA))
    
    is_find = False
    int_num = 0
   
    list_line = res.text.split("\n")
    for int_i, str_line in enumerate(list_line):
    
        # 종목 코드, 이름 발견 시
        if PARSER_CODE in str_line:
            str_code = str_line.split("=")[2].split('"')[0]
            str_name = str_line.split(">")[2].split("<")[0]
            
            is_find = True
            int_num = 0
            
        # 숫자 발견시
        elif is_find:
            if "number" in str_line:
                int_num += 1
                
                # 종가 정보 저장
                if int_num == IDX_CLOSE:
                    int_close = int(str_line.split(">")[1].split("<")[0].replace(",", "").strip())
                # 전일 가격 차이 정보 저장
                elif int_num == IDX_DELTA:
                    try:
                        int_delta = int(list_line[int_i + 2].replace(",", "").strip())
                    except ValueError:
                        int_delta = 0
                    except Error:
                        print("파싱 오류!")
                        sys.exit(1)
                # 전일 가격 차이(% 단위) 저장
                elif int_num == IDX_PERCENT:
                    try:
                        float_percent = float(list_line[int_i + 2].strip()[: -1])
                    except ValueError:
                        float_percent = 0
                    except Error:
                        print("파싱 오류!")
                        sys.exit(1)
                # 거래대금 정보 저장
                elif int_num == IDX_VOLUME:
                    int_volume = int(str_line.split(">")[1].split("<")[0].replace(",", "").strip())
                # 시가 정보 저장
                elif int_num == IDX_OPEN:
                    int_open = int(str_line.split(">")[1].split("<")[0].replace(",", "").strip())
                # 고가 정보 저장
                elif int_num == IDX_HIGH:
                    int_high = int(str_line.split(">")[1].split("<")[0].replace(",", "").strip())
                # 저가 정보 저장
                elif int_num == IDX_LOW:
                    int_low = int(str_line.split(">")[1].split("<")[0].replace(",", "").strip())
                # 시가총액 정보 저장
                elif int_num == IDX_SUM:
                    int_sum = int(str_line.split(">")[1].split("<")[0].replace(",", "").strip())
                    is_find = False
                    
                    dic_item[str_code] = {"type": int_type, "name": str_name, "close": int_close, "delta": int_delta, "percent": float_percent, "volume": int_volume, "open": int_open, "high": int_high, "low": int_low, "sum": int_sum}
            
"""
종목 정보 파일에 저장
"""
def saveFile(file, dic_item):
    file.write("종목 코드, 종목 이름, 타입(0: 코스피 1: 코스닥), 시가총액 (백만), 거래대금 (백만), 전일 차이(가격), 전일 차이(%), 종가, 시가, 고가, 저가\n")
    for str_code in dic_item.keys():
        str_name = dic_item[str_code]["name"]
        int_type = dic_item[str_code]["type"]
        int_sum = dic_item[str_code]["sum"]
        int_volume = dic_item[str_code]["volume"]
        int_delta = dic_item[str_code]["delta"]
        float_percent = dic_item[str_code]["percent"]
        int_close = dic_item[str_code]["close"]
        int_open = dic_item[str_code]["open"]
        int_high = dic_item[str_code]["high"]
        int_low = dic_item[str_code]["low"]
        file.write("%s, %s, %d, %d, %d, %d, %.2f, %d, %d, %d, %d\n" % (str_code, str_name, int_type, int_sum, int_volume, int_delta, float_percent, int_close, int_open, int_high, int_low))

"""
다운로드 함수
"""
def downloadFile():

    # 가장 최신 파일 찾기
    file_recent = None
    try:
        list_data = os.listdir("data")
        list_data.sort(reverse = True)
        file_recent = "data/" + list_data[0]
    except:
        pass
        
    # 종목 정보를 저장할 딕셔너리
    dic_item = {}

    # 코스피 종목 정보 저장
    int_last_kospi = getLastPage(TYPE_KOSPI)
    for int_page in range(1, int_last_kospi + 1):
        saveItemInfo(dic_item, TYPE_KOSPI, int_page)
    
    # 코스닥 종목 정보 저장
    int_last_kosdaq = getLastPage(TYPE_KOSDAQ)    
    for int_page in range(1, int_last_kosdaq + 1):
        saveItemInfo(dic_item, TYPE_KOSDAQ, int_page)
    
    # data 폴더 없으면 생성
    if os.path.isdir("data") is False:
        os.makedirs("data")
    
    # 이전 파일이 하나도 없으면 년월일.csv로 저장
    if file_recent == None:
        file = open(datetime.datetime.today().strftime("data/%Y%m%d.csv"), "w")
        saveFile(file, dic_item)
        file.close()
    # 이전 파일이 있다면 임시로 파일 저장 후 비교 후 년월일.csv로 저장
    else:
        file = open("data/temp.csv", "w")
        saveFile(file, dic_item)
        file.close()
        
        if filecmp.cmp(file_recent, "data/temp.csv") is False:
            os.system("mv data/temp.csv %s" % datetime.datetime.today().strftime("data/%Y%m%d.csv"))
            print("파일 다운로드 완료")
        else:
            print("파일이 이미 업데이트 되었습니다")
        os.system("rm data/temp.csv")
