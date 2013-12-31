#!/usr/bin/env python
#encoding=utf-8

from RenrenHandler import RenrenHandler
from dataMiningHandler import dataMiningHandler
from dataVisualizationHandler import dataVisualizationHandler
import sys, os, time, chardet
import pdb

if __name__ == '__main__':
	print "***********************************************"
	print "************RenrenDataRepo v1.0****************"
	print "***********************************************"
	print "console<<<all user datas are saved under config folder..."
	print "console<<<you need to guarantee you have access to the Internet..."
	print "\n"

	option = None
	NewDatasFlag = True
	while(option == None):
		print "console<<<whether to capture latest datas from the Internet even there exists local datas?(Y or N)"
		option = raw_input('> ')
		if not option in ["Y", "N"]:
			print "console<<<you input wrong option..."
			continue
		elif option == "Y":
			NewDatasFlag = True
		elif option == "N":
			NewDatasFlag = False
		else:
			print "console<<<unknown error!"
			time.sleep(5)
			sys.exit()

	print "console<<<please input your username..."
	username = raw_input('> ')
	print "please input your password..."
	password = raw_input('> ')

	myRenren = RenrenHandler(username=username, password=password)
	if not myRenren.userId:
		print "console<<<failed to login..."
		time.sleep(5)
		sys.exit()
	else:
		print "console<<<succeeded to login..."
		if NewDatasFlag:
			if os.path.exists("config/"+myRenren.userId):
				# pdb.set_trace()
				for root, dirs, files in os.walk("config/"+myRenren.userId, topdown=False):
					for name in files:
						try:
							os.remove(os.path.join(root, name))
						except:
							pass
					for name in dirs:
						try:
							os.rmdir(os.path.join(root, name))
						except:
							pass

		print "console<<<we provide you with functions as follows:"
		while(1):
			print "console<<<1:get your friends relation graph 2:recommand public pages according to friends 3:quit"
			option = raw_input('> ')
			try:
				option = int(option)
			except:
				print "console<<<you input wrong option..."
				continue

			if not option in [1,2,3]:
				print "console<<<you input wrong option..."
				continue
			else:
				if option == 3:
					print "console<<<quit..."
					sys.exit()
				elif option == 1:
					print "console<<<we are trying hard to generate the friends relation graph for you, please wait in patience..."
					myFriendsDict = myRenren.getFriendsDict(myRenren.userId)
					myDataVisualizationHandler = dataVisualizationHandler()
					myDataVisualizationHandler.import_data(myRenren, myFriendsDict)
					myDataVisualizationHandler.save()
					print "console<<succeeded to generate the friends relation graph..."
					print "console<<<you can find these files:" + "./config/" + myRenren.userId + "/data/friendsRelation.dot" + ", "+ "./config/" + myRenren.userId + "/data/friendsRelation.png"
				elif option == 2:
					print "console<<<we are trying hard to recommand public pages for you, please wait in patience..."
					myFriendsDict = myRenren.getFriendsDict(myRenren.userId)
					mydataMiningHandler = dataMiningHandler()
					k = 10#recommand top 10 in dafault
					optimalList = mydataMiningHandler.dataProcess(myRenren, myFriendsDict, k)
					if optimalList:
						totalFriendsNum = len(myFriendsDict)
						if k > len(optimalList):
							k = len(optimalList)
						# pdb.set_trace()
						codeType = chardet.detect(optimalList[0][0])["encoding"]
						print "console<<<top %s recommended public pages according to your friends:"%k
						for i in range(k):
							print optimalList[i][0] + "    you have " + "%.2f" %((float(optimalList[i][1])/float(totalFriendsNum))*100) + "% " + "friends notice the public page"
					else:
						print "console<<<you have no friends now, so we have no ability to recommand any public pages..."
				else:
					pass