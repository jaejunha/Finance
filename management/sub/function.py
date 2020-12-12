from sub.etc import *

import shutil
import copy
import matplotlib.pyplot as plt

from datetime import datetime

UNIT_MILLION = 1000000

def enterBaseDate(date_base):
	while True:
		try:
			temp_base = int(input("Base date (ex: " + str(date_base) + ") > "))
			if temp_base in list_date:
				date_base = temp_base
				break
			else:
				print("Please enter the correct date")
		except ValueError:
			print("Please enter the correct date")

	print("Base date is changed")
	input("Press any key if you go to main menu")

	return date_base

def showHistory(dic_data, list_date):
	list_x = []
	list_money = []
	list_frozen = []
		
	for date in list_date:
		list_x.append(str(date % 10000))
		dic_money, dic_frozen, list_temp = getInfo(dic_data, date)

		sum_money = 0
		for type in dic_money.keys():
			sum_money += dic_money[type]
		list_money.append(sum_money / UNIT_MILLION)

		sum_frozen = 0
		for type in dic_frozen.keys():
			sum_frozen += dic_frozen[type]
		list_frozen.append(sum_frozen / UNIT_MILLION)

	max_money = max(list_money)
	fig, ax = plt.subplots()
	ax.plot_date(list_x, list_money, marker='.', linestyle='-', label = "Collected")
	ax.plot_date(list_x, list_frozen, marker='.', linestyle='-', label = "Frozen")
	fig.autofmt_xdate()
	plt.ylim([0, max_money * 1.2])
	plt.xlabel('Date')
	plt.ylabel('Money [Million]')
	plt.legend(loc = "best")
	plt.show()

def copyData(dic_data, list_date):
	if len(list_date) == 1:
		print("There is no data to copy")
		input("Press any key if you go to main menu")
		return False

	str_date = datetime.today().strftime("%Y%m%d")
	int_date = int(str_date)
	last_date = list_date[-1]
	if (int_date in list_date) is False:
		list_date.append(int_date)
		dic_data[int_date] = copy.deepcopy(dic_data[last_date])
		print("Copy process is finished")
		input("Press any key if you go to main menu")
		return True
	else:
		print("Data exists")
		input("Press any key if you go to main menu")
		return False

def saveData(dic_data, list_date, date_base):
	str_date = datetime.today().strftime("%Y%m%d")
	# For backup
	shutil.copy("../_data/account.dat", "../_data/account_" + str_date + ".dat")

	file = open("../_data/account.dat", "w", encoding = "UTF8")
	len_date = len(list_date)
	for i, date in enumerate(list_date):
		line = "%d/content\n" % date

		line_sub = ""
		for dic in dic_data[date]:
			line_sub += "%s-%s:%d,%d" % (dic["name"], dic["type"], dic["frozen"], dic["money"])
			if "items" in dic.keys():
				line_sub += "{content}"
				line_items = ""
				for item in dic["items"]:
					line_items += "%s,%s,%d,%d-" % (item["code"], item["name"], item["frozen"], item["unit"])
				line_items = line_items[:-1]
				line_sub = line_sub.replace("content", line_items)
			line_sub += "/"
		line_sub = line_sub[:-1]
		line = line.replace("content", line_sub)
		if i == len_date - 1:
			line = line[:-1]
		file.write(line)
	file.close()

	file = open("../_data/base.dat", "w", encoding = "UTF8")
	file.write("%d" % date_base)
	file.close()

	print("Save process is finished")
	input("Press any key if you go to main menu")