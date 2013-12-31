#!/usr/bin/env python
#encoding=utf-8

import urllib
from httplib2 import Http
import re, chardet, json
import os, sys, time
# import pdb


class RenrenHandler(object):
    userId = None
    def __init__(self, username=None, 
            password=None, serveraddr="http://www.renren.com/"):
        self.__username = username
        self.__password = password
        self.__serveraddr = serveraddr
        self.__headerTemplate = {
            'Accept': 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5',
            'Accept-Charset': 'UTF-8,*;q=0.5',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.renren.com',
            'Referer': 'http://www.renren.com/Home.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.65 Safari/534.24',
        }

        self.__Login()#登录

    def __Login(self):
        self.myHttpHandler = Http()
        self.myHttpHandler.follow_redirects = False#失能重定向
        login_header = self.__headerTemplate.copy()
        login_header['Content-type'] = "application/x-www-form-urlencoded"
        login_data = {
            "email": self.__username,
            "password": self.__password,
            "origURL": self.__serveraddr + "home",
            "domain": "renren.com",
        }
        login_url = self.__serveraddr + "PLogin.do"
        try:
            resp, content = self.myHttpHandler.request(login_url, "POST", headers=login_header,
                          body=urllib.urlencode(login_data))
        except Exception, e:
            print e
            time.sleep(5)
            sys.exit()


        if resp['status'] == '302':
            self.header = self.__headerTemplate.copy()
            self.header['Cookie'] = resp['set-cookie']
        else:
            self.header = self.__headerTemplate.copy()
            self.header['Cookie'] = resp['set-cookie']

        tmptarget = re.search(" id=\d+[^;]", resp['set-cookie'])
        if tmptarget:
            self.userId = tmptarget.group(0)[4:]#obtain userId


    def __getFriends(self, uid):#need to connect to the Internet
        """Get the uid's friends and return the dict with uid as key,name as value."""
        # print "Geting %s friend list..." % str(uid)
        pagenum = 0
        friendsDict = {}
        friends_header = self.header.copy()
        friends_header["Host"] = "friend.renren.com"
        friends_header["Referer"] = "http://www.renren.com/" + uid

        while True:
            targetpage = "http://friend.renren.com/GetFriendList.do?curpage=" + str(pagenum) + "&id=" + str(uid)
            try:
                resp, content = self.myHttpHandler.request(targetpage, headers=friends_header)
            except Exception, e:
                print e
                print "get friends dict error!"
                time.sleep(5)
                sys.exit()
            pattern = '<a href="http://www\.renren\.com/profile\.do\?id=(\d+)"><img src="[\S]*" alt="[\S]*[\s]\((.*)\)" />'

            m = re.findall(pattern, content)
            if len(m) == 0:
                break
            for i in range(0, len(m)):
                fid = m[i][0]
                fname = m[i][1]
                #print fname, fid
                friendsDict[fid] = fname
            pagenum += 1
        # print "Got %s friends list successfully." % str(uid)


        return friendsDict

    def getFriendsDict(self, uid):
        """cache dict of uid in the disk."""
        try:#get datas from local disk
            with open("config/"+self.userId+"/"+uid+"/friendsDict.dat", 'r') as f:
                friendsDict = json.loads(f.read())
        except:#get datas from the Internet
            if not os.path.exists("config/"+self.userId+"/"+uid):
                os.makedirs("config/"+self.userId+"/"+uid)
            f = open("config/"+self.userId+"/"+uid+"/friendsDict.dat", 'w')
            # print "your friendsDict does not exist in disk, trying to get from Internet..."
            friendsDict = self.__getFriends(uid)
            friendsDict_json = json.dumps(friendsDict, ensure_ascii=False)
            f.write(friendsDict_json)
            friendsDict = json.loads(friendsDict_json)#得到utf-8编码的friendsDict
        f.close()
        # print friendsDict
        return friendsDict

    def getrelations(self, uid1, uid2):
        """receive two user id, If they are friends, return True, otherwise False."""
        dict_uid1 = self.getFriendsDict(uid1)
        if uid2 in dict_uid1:
            return True
        else:
            return False

    def __getPublicPages(self, uid):#need to connect to the Internet
        targetpage = "http://page.renren.com/home/friendspages/view?uid=" + uid
        targetheader = self.header.copy()
        targetheader["Host"] = "page.renren.com"
        targetheader["Referer"] = "http://www.renren.com/389748479/profile"
        try:
            resp, content = self.myHttpHandler.request(targetpage, headers=targetheader)
        except Exception, e:
            print e
            print "get public pages error!"
            time.sleep(5)
            sys.exit()
        # print content
        pattern = '<a class="owner" href="/\d+">(.*)</a>'

        m = re.findall(pattern, content)
        publicPagesDict = {}
        if len(m) == 0:
            return publicPagesDict
        else:
            codeType = chardet.detect(m[0][:(m[0].find('<'))])['encoding']
            for i in range(0, len(m)):
                publicPagesDict[i] =  m[i][:(m[i].find('<'))]#.decode(codeType).encode('gb2312')
            return publicPagesDict

    def getPublicPagesDict(self, uid):
        """cache dict of uid in the disk."""
        try:#get datas from local disk
            with open("config/"+self.userId+"/"+uid+"/publicPagesDict.dat", 'r') as f:
                publicPagesDict = json.loads(f.read())
        except:#get datas from the Internet
            if not os.path.exists("config/"+self.userId+"/"+uid):
                os.makedirs("config/"+self.userId+"/"+uid)
            f = open("config/"+self.userId+"/"+uid+"/publicPagesDict.dat", 'w')
            # print "your publicPagesDict does not exist in disk, trying to get from Internet..."
            publicPagesDict = self.__getPublicPages(uid)
            publicPagesDict_json = json.dumps(publicPagesDict, ensure_ascii=False)
            f.write(publicPagesDict_json)#加ensure_ascii=False后可以正确dumps
            # publicPagesDict = json.loads(publicPagesDict_json)
        f.close()
        # print publicPagesDict
        return publicPagesDict

if __name__ == '__main__':
    username = "yourusername"
    password = "yourpassword"
    myRenren = RenrenHandler(username=username, password=password)
    myRenren.getFriendsDict(myRenren.userId)
    myRenren.getrelations("uid1", "uid2")
    myRenren.getPublicPagesDict(myRenren.userId)