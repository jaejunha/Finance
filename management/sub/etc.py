from datetime import datetime

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

	try:
		file = open("../_data/base.dat", "r", encoding = "UTF8")
		date_base = int(file.readlines()[0])
		print(date_base)
		file.close()
	except FileNotFoundError:
		date_base = list_date[0]

	return dic_data, list_date, date_base

def getInfo(dic_data, day):
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