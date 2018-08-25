import os

import http as HTTP

clear = lambda: os.system('cls')

def printMenu():
	clear()
	print 
	print 'Finance Management Program'
	print 
	HTTP.printValueOfKOSPI200()
	print '======================================='
	print '1. Random KOSPI 200'
	print '2. Portfolio'
	print '3. Exit'
	print '======================================='