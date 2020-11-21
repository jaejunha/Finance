import os
import sys
import copy
import shutil
import matplotlib.pyplot as plt

from datetime import datetime

UNIT_MILLION = 1000000

def initializeData():
	list_date = []
	dic_data = {}
	try:
		file = open("../_data/account.dat", "r", encoding = "UTF8")
		for line in file.readlines():
			list_ele = line.split("/")
			int_date = int(list_ele[0])
			list_date.append(int_date)
			dic_data[int_date] = []

			len_ele = len(list_ele)
			for i in range(1, len_ele):
				raw_name_type = list_ele[i].split(":")[0].split("-")
				str_name = raw_name_type[0]
				str_type = raw_name_type[1]
				raw_frozen_money_item = list_ele[i].split(":")[1]
				if "{" in raw_frozen_money_item:
					raw_frozen_money = raw_frozen_money_item.split("{")[0].split(",")
					raw_list_item = raw_frozen_money_item.split("{")[1][:-1].split("-")

					list_item = []
					for raw_item in raw_list_item:
						raw_item_ele = raw_item.split(",")
						str_code = raw_item_ele[0]
						# 위의 str_name과 이름 겹쳐서 str_name -> str_item
						str_item = raw_item_ele[1]
						int_frozen = int(raw_item_ele[2])
						int_unit = int(raw_item_ele[3])
						list_item.append({"code": str_code, "name": str_item, "frozen": int_frozen, "unit": int_unit})
					int_frozen = int(raw_frozen_money[0])
					int_money = int(raw_frozen_money[1])
					dic_data[int_date].append({"name": str_name, "type": str_type, "frozen": int_frozen, "money": int_money, "items": list_item})
				else:
					raw_frozen_money = raw_frozen_money_item.split(",")
					int_frozen = int(raw_frozen_money[0])
					int_money = int(raw_frozen_money[1])
					dic_data[int_date].append({"name": str_name, "type": str_type, "frozen": int_frozen, "money": int_money})

		file.close()
	except FileNotFoundError:
		file = open("../_data/account.dat", "w", encoding = "UTF8")
		str_date = datetime.today().strftime("%Y%m%d")
		file.write(str_date)
		list_date.append(int(str_date))
		dic_data[int(str_date)] = []

	return list_date, dic_data

def getInfo(day):
	dic_money = {}
	dic_frozen = {}
	list_frozen = []
	for dic_ele in dic_data[day]:
		str_type = dic_ele["type"]
		if str_type in dic_money:
			dic_money[str_type] += dic_ele["money"]
		else:
			dic_money[str_type] = dic_ele["money"]
		if str_type in dic_frozen:
			dic_frozen[str_type] += dic_ele["frozen"]
		else:
			dic_frozen[str_type] = dic_ele["frozen"]
		if "items" in dic_ele.keys():
			for dic in dic_ele["items"]:
				list_frozen.append(dic)

	return dic_money, dic_frozen, list_frozen

def printScreen(list_date, dic_data, flag_save):
	list_date.sort()
	day_first = list_date[0]
	day_last = list_date[-1]

	dic_money, dic_frozen, list_frozen = getInfo(day_last)
	sum_money = 0
	sum_bank = 0
	for type in dic_money.keys():
		sum_money += dic_money[type]
		if type == "bank":
			sum_bank += dic_money[type]
	sum_frozen = 0
	for type in dic_frozen.keys():
		sum_frozen += dic_frozen[type]

	os.system("cls")
	print("\x1b[1;37;40m", end = "")
	print("Management program")
	print("\x1b[0m", end = "")
	print("=" * 30)
	print("Date\t%4d-%2d-%2d" %(day_last / 10000, day_last % 10000 / 100, day_last % 100))

	if day_last > day_first:
		dic_first_money = getInfo(day_first)[0]
		sum_first_money = 0
		sum_first_bank = 0
		for type in dic_first_money.keys():
			sum_first_money += dic_first_money[type]
			if type == "bank":
				sum_first_bank += dic_first_money[type]
		delta =  (sum_money - sum_first_money) / sum_money * 100
		if delta > 0:
			print("Total\t%s won (▲%.2f%%)" % ( format(sum_money, ","), delta ))
		elif delta == 0:
			print("Total\t%s won (-%.2f%%)" % ( format(sum_money, ","), 0 ))
		else:
			print("Total\t%s won (▼%.2f%%)" % ( format(sum_money, ","), delta ))
	else:
		print("Total\t%s won" % format(sum_money, ","))
		
	if sum_frozen == 0:
		print("Avail\t%s won (100.00%%)" % format(sum_money, ","))
		
	else:
		print("Avail\t%s won (%.2f%%)" % ( format(sum_money - sum_frozen, ","), (sum_money - sum_frozen) / sum_money * 100) )
		print()
		delta_bank = (sum_bank - sum_first_bank) / sum_bank * 100
		if delta_bank < 0:
			print("Bank\t▼%.2f%%" % delta_bank)
		elif delta_bank == 0:
			print("Bank\t-%.2f%%" % delta_bank)
		else:
			print("Bank\t▲%.2f%%" % delta_bank)
		delta_other = ((sum_money - sum_bank) - (sum_first_money - sum_first_bank)) / (sum_money - sum_bank) * 100
		if delta_other < 0:
			print("Other\t▼%.2f%%" % delta_other)
		elif delta_other == 0:	
			print("Other\t-%.2f%%" % delta_other)
		else:
			print("Other\t▲%.2f%%" % delta_other)
				
		print("-" * 30)
		print("\x1b[2;37;44m", end = "")
		print("Frozen list ▼")
		print("\x1b[0m", end = "")
		for dic_frozen in list_frozen:
			print(" - %s: %s won" % (dic_frozen["name"], format(dic_frozen["frozen"], ",")))
	print("=" * 30)
	print()
	print("\x1b[1;37;40m", end = "")
	print("Menu")
	print("\x1b[0m", end = "")
	print("=" * 30)
	print("1. Show History")
	print("-" * 30)
	print("\x1b[30m", end = "")
	print("2. Add new Account type")
	print("3. Modify Account type")
	print("4. Delete Account type")
	print("\x1b[0m", end = "")
	print("5. Copy all previous contents")
	print("\x1b[30m", end = "")
	print("6. Modify Account contents")
	print("7. Delete Account contents")
	print("\x1b[0m", end = "")
	print("-" * 30)
	if flag_save:
		print("\x1b[1;31;41m", end = "")
		print("8. Save current state")
		print("\x1b[0m", end = "")
	else:
		print("8. Save current state")
	print("9. Exit Program")
	print("=" * 30)

def showHistory(list_date):
	list_x = []
	list_money = []
	list_frozen = []
		
	for date in list_date:
		list_x.append(date % 10000)
		dic_money, dic_frozen, list_temp = getInfo(date)

		sum_money = 0
		for type in dic_money.keys():
			sum_money += dic_money[type]
		list_money.append(sum_money / UNIT_MILLION)

		sum_frozen = 0
		for type in dic_frozen.keys():
			sum_frozen += dic_frozen[type]
		list_frozen.append(sum_frozen / UNIT_MILLION)

	max_money = max(list_money)
	plt.ylim([0, max_money * 1.2])
	plt.plot(list_x, list_money, label = "Collected")
	plt.plot(list_x, list_frozen, label = "Frozen")
	plt.xlabel('Date')
	plt.ylabel('Money [Million]')
	plt.legend(loc = "best")
	plt.show()

def copyData(list_date, dic_data):
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

def saveData(list_date, dic_data):
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
	print("Save process is finished")
	input("Press any key if you go to main menu")

if __name__=="__main__":
	
	flag_save = False
	list_date, dic_data = initializeData()
	while True:
		printScreen(list_date, dic_data, flag_save)
		while True:
			try:
				select = int(input("Select > "))
				break
			except ValueError:
				print("Please enter the correct number")
		if select == 1:
			showHistory(list_date)
		elif select == 5:
			flag_save = copyData(list_date, dic_data)
		elif select == 8:
			flag_save = False
			saveData(list_date, dic_data)
		elif select == 9:
			sys.exit()
		