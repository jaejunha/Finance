import sys

def readData():
	dic_data = {}
	list_date = []

	file = open(sys.argv[1], "r")

	for str_line in file.readlines():
		list_ele = str_line.split(",")
		int_date = int(list_ele[0].strip())
		int_end = int(list_ele[1].strip())
		int_start = int(list_ele[2].strip())
		int_high = int(list_ele[3].strip())
		int_low = int(list_ele[4].strip())
	
		list_date.append(int_date)
		dic_data[int_date] = {"end": int_end, "start": int_start, "high": int_high, "low": int_low}

	file.close()
	
	return list_date, dic_data

def saveDay(list_date, dic_data):
	str_code = sys.argv[1].split("_")[0]

	list_date.sort()
	sum_5 = 0
	sum_20 = 0
	sum_60 = 0
	sum_120 = 0
	sum_240 = 0	

	for i, int_date in enumerate(list_date):
		if i >= 5:
			sum_5 -= dic_data[list_date[i - 5]]["end"]	
		if i >= 20:
			sum_20 -= dic_data[list_date[i - 20]]["end"]
		if i >= 60:
			sum_60 -= dic_data[list_date[i - 60]]["end"]
		if i >= 120:
			sum_120 -= dic_data[list_date[i - 120]]["end"]
		if i >= 240:
			sum_240 -= dic_data[list_date[i - 240]]["end"]

		int_end = dic_data[int_date]["end"]
		
		sum_5 += int_end
		sum_20 += int_end
		sum_60 += int_end
		sum_120 += int_end
		sum_240 += int_end

		if i >= 5 - 1:
			dic_data[int_date]["ma5"] = sum_5 / 5
		else:
			dic_data[int_date]["ma5"] = 0

		if i >= 20 - 1:
			dic_data[int_date]["ma20"] = sum_20 / 20
		else:
			dic_data[int_date]["ma20"] = 0

		if i >= 60 - 1:
			dic_data[int_date]["ma60"] = sum_60 / 60
		else:
			dic_data[int_date]["ma60"] = 0

		if i >= 120 - 1:
			dic_data[int_date]["ma120"] = sum_120 / 120
		else:
			dic_data[int_date]["ma120"] = 0

		if i >= 240 - 1:
			dic_data[int_date]["ma240"] = sum_240 / 240
		else:
			dic_data[int_date]["ma240"] = 0

	list_date.sort(reverse = True)

	file = open(str_code + "_day.csv", "w")
	
	file.write("날짜, 종가, 시가, 고가, 저가, MA5, MA20, MA60, MA120, MA240\n")
	for int_date in list_date:
		file.write("%d, %d, %d, %d, %d, %d, %d, %d, %d, %d\n" % (int_date, dic_data[int_date]["end"], dic_data[int_date]["start"], dic_data[int_date]["high"], dic_data[int_date]["low"], dic_data[int_date]["ma5"], dic_data[int_date]["ma20"], dic_data[int_date]["ma60"], dic_data[int_date]["ma120"], dic_data[int_date]["ma240"]))
	 
	file.close()

def saveYear(list_date, dic_data):
	str_code = sys.argv[1].split("_")[0]

	list_year = []
	dic_year = {}
	key_year = None
	list_date.sort()
	for int_date in list_date:
		int_year = int(int_date / 10000)
		if key_year != int_year:
			key_year = int_year
			dic_year[int_year] = {"date": int_date, "end": dic_data[int_date]["end"], "high": dic_data[int_date]["high"], "low": dic_data[int_date]["low"]}
			list_year.append(int_year)
		else:
			if dic_year[int_year]["high"] < dic_data[int_date]["high"]:
				dic_year[int_year]["high"] = dic_data[int_date]["high"]
	
			if dic_year[int_year]["low"] > dic_data[int_date]["low"] and dic_data[int_date]["low"] != 0:
				dic_year[int_year]["low"] = dic_data[int_date]["low"]

	file = open(str_code + "_year.csv", "w")
	file.write("수익률A, 이전년도 첫날 사서 해당년도 첫날 팔 경우\n")
	file.write("수익률B, 이전년도 저가 사서 해당년도 고가 팔 경우\n")
	file.write("수익률C, 이전년도 고가 사서 해당년도 저가 팔 경우\n")
	file.write("년도, 첫날, 종가, 고가, 저가, 수익률A, 수익률B, 수익률C, 수익률 범위\n") 
	for i, int_year in enumerate(list_year):
		if i == 0:
			file.write("%d, %d, %d, %d, %d\n" % (int_year, dic_year[int_year]["date"], dic_year[int_year]["end"], dic_year[int_year]["high"], dic_year[int_year]["low"]))
		else:
			pre_year = list_year[i - 1]
			int_normal = ((dic_year[int_year]["end"] - dic_year[pre_year]["end"]) / dic_year[pre_year]["end"]) * 100
			int_max = ((dic_year[int_year]["high"] - dic_year[pre_year]["low"]) / dic_year[pre_year]["low"]) * 100
			int_min = ((dic_year[int_year]["low"] - dic_year[pre_year]["high"]) / dic_year[pre_year]["high"]) * 100
			file.write("%d, %d, %d, %d, %d, %.2f%%,  %.2f%%,  %.2f%%,  %.2f%% ~ %.2f%%\n" % (int_year, dic_year[int_year]["date"], dic_year[int_year]["end"], dic_year[int_year]["high"], dic_year[int_year]["low"], int_normal, int_max, int_min, int_min, int_max))
	file.close()

if __name__ == "__main__":
	list_date, dic_data = readData()
	saveDay(list_date, dic_data)
	saveYear(list_date, dic_data)
