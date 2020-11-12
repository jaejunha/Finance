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

if __name__=="__main__":
	list_date.sort()
	last_date = list_date[-1]

	sum_money = 0
	sum_frozen = 0
	list_frozen = []
	for dic_ele in dic_data[last_date]:
		sum_money += dic_ele["money"]
		sum_frozen += dic_ele["frozen"]
		if "items" in dic_ele.keys():
			for dic_frozen in dic_ele["items"]:
				list_frozen.append(dic_frozen)
	if sum_frozen == 0:
		print("%4d-%2d-%2d, Total: %s won (Available: 100.00%%)" % (last_date / 10000, last_date % 10000 / 100, last_date % 100, format(sum_money, ",")))
		
	else:
		print("%4d-%2d-%2d, Total: %s won (Available: %.2f%%)" % (last_date / 10000, last_date % 10000 / 100, last_date % 100, format(sum_money, ","), (sum_money - sum_frozen) / sum_money * 100))

	if len(list_frozen) > 0:
		print("Frozen list ▼")
		for dic_frozen in list_frozen:
			print(" - %s: %s won" % (dic_frozen["name"], format(dic_frozen["frozen"], ",")))
	print()
	print("Menu")
	print("1. Add Account")
	print("2. Update Account")
	print("3. Delete Account")
	print("4. Save Account")
	print("5. Exit Program")