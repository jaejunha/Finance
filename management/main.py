import os
import matplotlib.pyplot as plt

from datetime import datetime

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
					str_name = raw_item_ele[1]
					int_frozen = int(raw_item_ele[2])
					int_unit = int(raw_item_ele[3])
					list_item.append({"code": str_code, "name": str_name, "frozen": int_frozen, "unit": int_unit})
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

def getInfo(day):
	sum_money = 0
	sum_frozen = 0
	list_frozen = []
	for dic_ele in dic_data[day]:
		sum_money += dic_ele["money"]
		sum_frozen += dic_ele["frozen"]
		if "items" in dic_ele.keys():
			for dic_frozen in dic_ele["items"]:
				list_frozen.append(dic_frozen)

	return sum_money, sum_frozen, list_frozen

if __name__=="__main__":
	list_date.sort()
	day_first = list_date[0]
	day_last = list_date[-1]

	sum_money, sum_frozen, list_frozen = getInfo(day_last)

	while True:
		os.system("cls")
		print("Management program")
		print("=" * 30)
		print("Date\t%4d-%2d-%2d" %(day_last / 10000, day_last % 10000 / 100, day_last % 100))

		if day_last > day_first:
			sum_first_money = getInfo(day_first)[0]
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
			print("-" * 30)
			print("Frozen list ▼")
			for dic_frozen in list_frozen:
				print(" - %s: %s won" % (dic_frozen["name"], format(dic_frozen["frozen"], ",")))
		print("=" * 30)
		print()
		print("Menu")
		print("=" * 30)
		print("1. Show History")
		print("2. Add Account")
		print("3. Update Account")
		print("4. Delete Account")
		print("5. Save Account")
		print("6. Exit Program")
		print("=" * 30)
		while True:
			try:
				select = int(input("Select > "))
				break
			except ValueError:
				print("Please enter the correct number")
		if select == 1:
			list_x = []
			list_y = []
			for date in list_date:
				list_x.append(date % 10000)
				list_y.append(getInfo(date)[0])
			plt.plot(list_x, list_y)
			plt.show()
		