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
