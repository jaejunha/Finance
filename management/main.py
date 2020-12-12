from sub.function import *
from sub.etc import *

import os
import sys

def printScreen(dic_data, list_date, day_base, flag_save):
	list_date.sort()
	day_last = list_date[-1]

	dic_money, dic_frozen, list_frozen = getInfo(dic_data, day_last)
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
	print("Date\t%4d-%02d-%02d (base: %4d-%02d-%02d)" %(day_last / 10000, day_last % 10000 / 100, day_last % 100, day_base / 10000, day_base % 10000 / 100, day_base % 100))

	if day_last > day_base:
		dic_base_money = getInfo(dic_data, day_base)[0]
		sum_base_money = 0
		sum_base_bank = 0
		for type in dic_base_money.keys():
			sum_base_money += dic_base_money[type]
			if type == "bank":
				sum_base_bank += dic_base_money[type]
		delta =  (sum_money - sum_base_money) / sum_money * 100
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
		delta_bank = (sum_bank - sum_base_bank) / sum_bank * 100
		if delta_bank < 0:
			print("Bank\t▼%.2f%%" % delta_bank)
		elif delta_bank == 0:
			print("Bank\t-%.2f%%" % delta_bank)
		else:
			print("Bank\t▲%.2f%%" % delta_bank)
		delta_other = ((sum_money - sum_bank) - (sum_base_money - sum_base_bank)) / (sum_money - sum_bank) * 100
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
	print(" 1. Set Base date")
	print(" 2. Show History")
	print("-" * 30)
	print("\x1b[30m", end = "")
	print(" 3. Add new Account type")
	print(" 4. Modify Account type")
	print(" 5. Delete Account type")
	print("\x1b[0m", end = "")
	print(" 6. Copy all previous contents")
	print("\x1b[30m", end = "")
	print(" 7. Modify Account contents")
	print(" 8. Delete Account contents")
	print("\x1b[0m", end = "")
	print("-" * 30)
	if flag_save:
		print("\x1b[1;31;41m", end = "")
		print(" 9. Save current state")
		print("\x1b[0m", end = "")
	else:
		print(" 9. Save current state")
	print("10. Exit Program")
	print("=" * 30)

if __name__=="__main__":
	
	flag_save = False
	dic_data, list_date, date_base = initializeData()
	while True:
		printScreen(dic_data, list_date, date_base, flag_save)
		while True:
			try:
				select = int(input("Select > "))
				break
			except ValueError:
				print("Please enter the correct number")
		if select == 1:
			flag_save = True
			date_base = enterBaseDate(date_base)
		elif select == 2:
			showHistory(dic_data, list_date)
		elif select == 6:
			flag_save = copyData(dic_data, list_date)
		elif select == 9:
			flag_save = False
			saveData(dic_data, list_date, date_base)
		elif select == 10:
			sys.exit()
		