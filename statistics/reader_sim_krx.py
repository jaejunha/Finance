import sys

"""
Read CSV from Crwaling data
"""
list_date = []
dic_data = {}
file = open(sys.argv[1], "r")
for i, line in enumerate(file.readlines()):
    if i == 0:
        continue
    
    try:
        list_ele = line.split(",")
        int_date = int(list_ele[0].replace("/", "").strip())
        float_close = float(list_ele[1].strip())
        dic_data[int_date] = {"close": float_close}
        list_date.append(int_date)
    except Exception as e:
        print(e)
list_date.sort()

"""
Calculate MA
"""
sum_5 = 0
sum_20 = 0
sum_60 = 0
sum_120 = 0
for i, date in enumerate(list_date):
    sum_5 += dic_data[date]["close"]
    sum_20 += dic_data[date]["close"]
    sum_60 += dic_data[date]["close"]
    sum_120 += dic_data[date]["close"]
    
    if i >= 5:
        sum_5 -= dic_data[list_date[i - 5]]["close"]
        dic_data[date]["ma5"] = sum_5 / 5
    if i >= 20:
        sum_20 -= dic_data[list_date[i - 20]]["close"]
        dic_data[date]["ma20"] = sum_20 / 20
    if i >= 60:
        sum_60 -= dic_data[list_date[i - 60]]["close"]
        dic_data[date]["ma60"] = sum_60 / 60
    if i >= 120:
        sum_120 -= dic_data[list_date[i - 120]]["close"]
        dic_data[date]["ma120"] = sum_120 / 120
        
"""
Find Similarity
"""
idx_now = len(list_date) - 1
list_sim = []
for i in range(120, idx_now):
    date_com = list_date[i]
    date_now = list_date[idx_now]
    
    diff_5 = abs( (dic_data[date_now]["ma5"] - dic_data[date_now]["close"]) / dic_data[date_now]["close"] - (dic_data[date_com]["ma5"] - dic_data[date_com]["close"]) / dic_data[date_com]["close"] ) * 100
    diff_20 = abs( (dic_data[date_now]["ma20"] - dic_data[date_now]["close"]) / dic_data[date_now]["close"] - (dic_data[date_com]["ma20"] - dic_data[date_com]["close"]) / dic_data[date_com]["close"] ) * 100
    diff_60 = abs( (dic_data[date_now]["ma60"] - dic_data[date_now]["close"]) / dic_data[date_now]["close"] - (dic_data[date_com]["ma60"] - dic_data[date_com]["close"]) / dic_data[date_com]["close"] ) * 100
    diff_120 = abs( (dic_data[date_now]["ma120"] - dic_data[date_now]["close"]) / dic_data[date_now]["close"] - (dic_data[date_com]["ma120"] - dic_data[date_com]["close"]) / dic_data[date_com]["close"] ) * 100
    
    list_sim.append( ((diff_5 + diff_20 + diff_60 + diff_120) / 4, date_com) )
list_sim.sort()
print(list_sim[0:9])
