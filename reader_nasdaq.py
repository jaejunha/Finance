import sys

MAX_VALUE = 999999999
UNIT_MONTH = 20

def readRawData(index):
	dic_data = {}
	list_date = []

	file = open(sys.argv[1], "r")
	for i, line in enumerate(file.readlines()):
		if i == 0:
			continue

		list_raw = line.strip().split(",")

		date = int(list_raw[0])
		list_date.append(date)
		
		if index == True:
			end = float(list_raw[4])
			start = float(list_raw[1])
			high = float(list_raw[2])
			low = float(list_raw[3])
		else:
			end = int(list_raw[4])
			start = int(list_raw[1])
			high = int(list_raw[2])
			low = int(list_raw[3])

		dic_data[date] = {"end": end, "start": start, "high": high, "low": low}
	file.close()

	list_date.sort()

	return list_date, dic_data

if __name__ == "__main__":
	list_date, dic_data = readRawData(True)

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

	print("날짜(년월일)", "바닥")
	list_floor = []
	for floor in list(cnt_floor.keys()):
		if cnt_floor[floor] >= UNIT_MONTH:
			list_floor.append((floor, date_floor[floor]))
			print(date_floor[floor], floor)

	list_floor.sort()
	
	list_month = list(dic_month)
	for month in list_month:
		print(month, dic_month[month]["low"], dic_month[month]["high"], (dic_month[month]["low"] - dic_month[month]["high"]) * 100.0 / dic_month[month]["high"])

	cur_floor = 0
	file = open("temp.csv", "w")
	file.write("날짜, 종가, 시가, 고가, 저가, 바닥, 바닥날짜\n")
	for i, date in enumerate(list_date):
		if date > list_floor[cur_floor][1] and (cur_floor < len(list_floor) - 1):
			cur_floor += 1
		file.write("%d, %f, %f, %f, %f, %f, %f\n" % (date, dic_data[date]["end"], dic_data[date]["start"], dic_data[date]["high"], dic_data[date]["low"], list_floor[cur_floor][0], list_floor[cur_floor][1]))