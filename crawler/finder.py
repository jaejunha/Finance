# -*- coding: UTF-8 -*-
import os

IDX_NAME = 1
IDX_VOLUME = 4
IDX_DELTA = 5
IDX_PERCENT = 6
IDX_CLOSE = 7
IDX_OPEN = 8
IDX_HIGH = 9
IDX_LOW = 10


"""
변동성 종목 찾기
"""
def getFluctuation(is_down, is_raw, float_rate):
    list_data = os.listdir("data")
    list_data.sort(reverse = True)
    
    file_recent = list_data[0]
    int_recent = int(file_recent.split(".")[0])
    str_recent = "%04d년 %02d월 %02d일" % (int_recent / 10000, (int_recent % 10000) / 100, int_recent % 100)
    file = open("data/" + file_recent, "r", encoding = "euc-kr")

    list_fluctuation_down = []
    list_fluctuation_up = []
    for int_i, str_line in enumerate(file.readlines()):
        if int_i == 0:
            continue

        try:
            ele_data = str_line.split(",")
            float_percent = float(ele_data[IDX_PERCENT].strip())
            int_open = int(ele_data[IDX_OPEN].strip())
            int_high = int(ele_data[IDX_HIGH].strip())
            int_low = int(ele_data[IDX_LOW].strip())

            float_percent_low = (int_low - int_open) / int_open * 100
            float_percent_high = (int_high - int_open) / int_open * 100

            if is_down:
                if (-float_percent_low > float_rate) and (float_percent_high > float_rate) and float_percent < 0:
                    list_fluctuation_down.append( (float_percent_high - float_percent_low, str_line.strip()) )
            else:
                if (-float_percent_low > float_rate) and (float_percent_high > float_rate) and float_percent > 0:
                    list_fluctuation_up.append( (float_percent_high - float_percent_low, str_line.strip()) )

        except:
            continue

    if is_down:
        list_fluctuation_down.sort(reverse = True)
        list_ret = list_fluctuation_down
    else:
        list_fluctuation_up.sort(reverse = True)
        list_ret = list_fluctuation_up

    if is_raw:
        return str_recent, list_ret
    else:
        str_html = '<table style="width: 100%;">'
        str_html += '<tr style="font-weight: bold;">'
        str_html += "<td>변동성</td>"
        str_html += "<td>종목명</td>"
        str_html += "<td>종가</td>"
        str_html += "<td>거래대금</td>"
        str_html += "<td>종가 - 저가</td>"
        str_html += "</tr>"
        for ele_ret in list_ret:

            str_html += "<tr>"

            float_fluctuation = ele_ret[0]
            str_html += "<td>%.2f %%</td>" % float_fluctuation
            str_line = ele_ret[1]

            list_ele = str_line.split(",")
            str_name = list_ele[IDX_NAME].strip()
            str_html += "<td>%s</td>" % str_name
           
            float_percent = float(list_ele[IDX_PERCENT].strip())
            str_html += "<td>%.2f %%</td>" % float_percent

            str_volume = format(int(list_ele[IDX_VOLUME].strip()), ",")
            str_html += "<td>%s 백만</td>" % str_volume

            if float_percent > 0:
                int_previous = int(list_ele[IDX_CLOSE].strip()) - int(list_ele[IDX_DELTA].strip())
            else:
                int_previous = int(list_ele[IDX_CLOSE].strip()) + int(list_ele[IDX_DELTA].strip())
            int_low = int(list_ele[IDX_LOW].strip())
            float_low = (int_low - int_previous) / int_previous * 100.0
            str_html += "<td>%.2f %%</td>" % abs(float_percent - float_low)

            str_html += "</tr>"
        str_html += "</table>"

        return str_recent, str_html
