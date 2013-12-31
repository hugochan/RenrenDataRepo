#!/usr/bin/env python
#coding=utf-8

from RenrenHandler import RenrenHandler
# import pdb

class dataMiningHandler(object):
	"""recommand public pages according to friens' preference"""
	def dataProcess(self, handler, data, k=1):
		# pdb.set_trace()
		optimalDict = {}
		optimalList = []
		totalFriendsNum = len(data)
		if totalFriendsNum > 0:
			for eachkey in data.keys():
				eachPagesDict = handler.getPublicPagesDict(eachkey)
				for eachvalue in eachPagesDict.values():
					if eachvalue not in optimalDict:
						optimalDict[eachvalue] = 1
					else:
						optimalDict[eachvalue] += 1
				# print eachkey
			optimalList = sorted(optimalDict.items(), key=lambda optimalDict:optimalDict[1], reverse=True)
			return optimalList
		else:
			return None


if __name__ == '__main__':
	username = "yourusername"
	password = "yourpassword"
	myRenren = RenrenHandler(username=username, password=password)
	myFriendsDict = myRenren.getFriendsDict(myRenren.userId)
	mydataMiningHandler = dataMiningHandler()
	mydataMiningHandler.dataProcess(myRenren, myFriendsDict, 10)