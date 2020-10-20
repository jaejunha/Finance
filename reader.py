"""
구현할 것▼
두꺼운 바닥 선 추가
"""
import sys

DATE_DIVISION = 20180000
UNIT_MILLION = 1000000
UNIT_ORIGIN = 50

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

	list_floor = []
	cnt_floor = {}
	length = len(list_date)
	floor_prev = None
	sum_diff = 0
	for i in range(0, length - 1):
		sum_diff += abs(dic_data[list_date[i + 1]]["end"] - dic_data[list_date[i]]["end"]) / dic_data[list_date[i]]["end"] * 100.0
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
		list_floor.append({"floor": floor_value, "date": floor_date})
	sum_diff /= (length - 1)
		
	print(sum_diff)

	for floor in list(cnt_floor.keys()):
		if cnt_floor[floor] < 20:
			del(cnt_floor[floor])

	print(cnt_floor)

	file = open("temp.csv", "w")
	file.write("날짜, 가격, 바닥, 바닥날짜\n")
	for i, date in enumerate(list_date):
		file.write("%d, %d, %d, %d\n" % (date, dic_data[date]["end"], list_floor[i]["floor"], list_floor[i]["date"]))