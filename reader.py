import sys

DATE_DIVISION = 20180000
UNIT_MILLION = 1000000
UNIT_ORIGIN = 50

"""
# For Samsung Electronics
# argv[1]: csv file
"""
dic_data = {}
list_date = []
file_r = open(sys.argv[1], "r")
file_w = open("result.csv", "w")
for line in file_r.readlines():
	list_raw = line.strip().split(",")

	date = int(list_raw[0])
	list_date.append(date)

	close = int(list_raw[1])
	open = int(list_raw[2])
	high = int(list_raw[3])
	low = int(list_raw[4])

	if (date >= DATE_DIVISION) and (close < UNIT_MILLION):
		close *= UNIT_ORIGIN
		open *= UNIT_ORIGIN
		high *= UNIT_ORIGIN
		low *= UNIT_ORIGIN

	dic_data[date] = {"close": close, "open": open, "high": high, "low": low}
file_r.close()

list_date.sort()

"""
Below line will be deleted
"""
file_w.write("날짜, 종가, 시가, 고가, 저가\n")
for date in list_date:
	file_w.write("%d, %d, %d, %d, %d\n" % (date, dic_data[date]["close"], dic_data[date]["open"], dic_data[date]["high"], dic_data[date]["low"]))