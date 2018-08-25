import util as UTIL
import menu as MENU
import dbms as DBMS

if __name__ == '__main__':
	bool_update = False
	list_kospi200 = []
	db_id, db_pwd, db_db, bool_error = DBMS.checkDB()

	while bool_error == False:
		UTIL.printMenu()
		str_menu = raw_input('Please select the MENU >> ')
		if str_menu == '1':
			bool_update, list_kospi200 = MENU.randomKOSPI200(db_id, db_pwd, db_db, bool_update, list_kospi200)
		elif str_menu == '2':
			pass
		elif str_menu == '3':
			print 'Good Bye!'
			break
		else:
			print 'Check your input'
			str_answer = raw_input('Please Enter the any key')


