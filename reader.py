"""
구현할 것▼
일반 적인 우상향 종목 (지수 ETF)에도 가능하도록 구현하기
고점이 바닥 대비 몇 %인지 (최대 손실 확인)
"""
import sys

DATE_DIVISION = 20180000
UNIT_MILLION = 1000000
UNIT_ORIGIN = 50
UNIT_MONTH = 20
MAX_VALUE = 999999999

"""
# For Samsung Electronics
# argv[1]: csv file
"""

def readRawData():
	dic_data = {}
	list_date = []

	file = open(sys.argv[1], "r")
	for line in file.readlines():
		list_raw = line.strip().split(",")

		date = int(list_raw[0])
		list_date.append(date)

		end = int(list_raw[1])
		start = int(list_raw[2])
		high = int(list_raw[3])
		low = int(list_raw[4])

		if (date >= DATE_DIVISION) and (end < UNIT_MILLION):
			end *= UNIT_ORIGIN
			start *= UNIT_ORIGIN
			high *= UNIT_ORIGIN
			low *= UNIT_ORIGIN

		dic_data[date] = {"end": end, "start": start, "high": high, "low": low}
	file.close()

	list_date.sort()

	return list_date, dic_data

def saveModifiedData(list_date, dic_data):
	code = sys.argv[1].split("_")[0]
	file = open(code + "_data.csv", "w")

	"""
	Below line will be deleted
	"""
	file.write("날짜, 종가, 시가, 고가, 저가\n")
	for date in list_date:
		file.write("%d, %d, %d, %d, %d\n" % (date, dic_data[date]["end"], dic_data[date]["start"], dic_data[date]["high"], dic_data[date]["low"]))

if __name__ == "__main__":
	list_date, dic_data = readRawData()
	saveModifiedData(list_date, dic_data)

	dic_month = {}
	cnt_floor = {}
	date_floor = {}
	length = len(list_date)
	floor_prev = None
	sum_diff = 0
	for i in range(0, length - 1):
		sum_diff += abs(dic_data[list_date[i + 1]]["end"] - dic_data[list_date[i]]["end"]) / dic_data[list_date[i]]["end"] * 100.0

		month = int(list_date[i] / 100)
		if month in dic_month.keys():
			if dic_data[list_date[i]]["low"] < dic_month[month]["low"]:
				if dic_data[list_date[i]]["low"] is not 0:
					dic_month[month]["low"] = dic_data[list_date[i]]["low"]
			if dic_data[list_date[i]]["high"] > dic_month[month]["high"]:
				dic_month[month]["high"] = dic_data[list_date[i]]["high"]
		else:
			dic_month[month] = {}
			dic_month[month]["low"] = MAX_VALUE
			dic_month[month]["high"] = 0

		floor_date = list_date[i]
		floor_value = dic_data[list_date[i]]["high"]
		for j in range(i + 1, length):
			if floor_value > dic_data[list_date[j]]["low"] and dic_data[list_date[j]]["low"] > 0:
				floor_value = dic_data[list_date[j]]["low"]
				floor_date = list_date[j]
		if floor_value == 0:
			floor_value = floor_prev
		else:
			floor_prev = floor_value
		if floor_value in cnt_floor.keys():
			cnt_floor[floor_value] += 1
		else:
			cnt_floor[floor_value] = 1
		date_floor[floor_value] = floor_date
	sum_diff /= (length - 1)
		
	print("평균 등락폭", sum_diff)

	print("날짜(년월일)", "바닥(분할전)", "바닥(분할후)")
	list_floor = []
	for floor in list(cnt_floor.keys()):
		if cnt_floor[floor] >= UNIT_MONTH:
			list_floor.append((floor, date_floor[floor]))
			print(date_floor[floor], floor, int(floor / 50))

	list_floor.sort()
	
	list_month = list(dic_month)
	for month in list_month:
		print(month, int(dic_month[month]["low"] / 50), int(dic_month[month]["high"] / 50), (dic_month[month]["low"] - dic_month[month]["high"]) * 100.0 / dic_month[month]["high"])

	cur_floor = 0
	file = open("temp.csv", "w")
	file.write("날짜, 종가, 시가, 고가, 저가, 바닥, 바닥날짜, 분할종가, 분할바닥\n")
	for i, date in enumerate(list_date):
		if date > list_floor[cur_floor][1] and (cur_floor < len(list_floor) - 1):
			cur_floor += 1
		file.write("%d, %d, %d, %d, %d, %d, %d, %d, %d\n" % (date, dic_data[date]["end"], dic_data[date]["start"], dic_data[date]["high"], dic_data[date]["low"], list_floor[cur_floor][0], list_floor[cur_floor][1], dic_data[date]["end"] / 50, list_floor[cur_floor][0] / 50))