#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import oss2
import requests
import sys

class Oss2bucket:
	def __init__(self):
		self.AK = "/etc/ossAK"
		self.endpoint = "oss-cn-shanghai.aliyuncs.com"
		self.bucketname = "scrapy-images"
		access = ((open(self.AK)).read()).split(',')
		self.auth = oss2.Auth(access[0],access[1])
		
	def listbucket(self):
		service = oss2.Service(self.auth, self.endpoint)
		return oss2.BucketIterator(service)
		
	def getbucket(self, bucketname=None):
		if bucketname == None:
			bucketname = self.bucketname
		names = ([b.name for b in self.listbucket()])
		if bucketname in names:
			return oss2.Bucket(self.auth, self.endpoint, bucketname)
		else:
			sys.exit("There is no such bucket")
			

class Spider:
	def __init__{self}:
		self.siteURL = "https://mm.taobao.com/tstar/search/tstar_model.do"
		
	def getPage(self,pageindex):
		payload = {'_input_charset':'utf-8','currentPage':pageindex}
		page = requests.post(self.siteURL, params=payload)
		if page.status_code == 200
			return page.text
		else:
			sys.exit("Cannot get the web page")
			
	def getAllimages(self,pageindex):
		page = self.getPage(pageindex)
		regex = '"cardUrl":"(//.+?)".*?"realName":"(.+?)",.*?"userId":(.*?),"'
		pattern = re.compile(regex, re.S)
		items = re.findall(pattern, page)
		
	def saveimage(self,image):
	
	def addimages(self,number,start_page=1):
		count = 0
		pageindex = start_page
		
		while count < number:
			items = self.getAllimages(pageindex)
			for item in items:
				imageURL = "https:" + item[0]
				