#！/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import oss2
import requests

class Spider:
	def __init__{self}:
		self.siteURL = "https://mm.taobao.com/tstar/search/tstar_model.do"
		
	def getPage(self,pageindex):
		payload = {'_input_charset':'utf-8','currentPage':pageindex}
		page = requests.post(self.siteURL, params=payload)
		if page.status 
		return page.
		
	def getAllimages(self,pageindex):
		page = self.getPage(pageindex)
		regex = '"cardUrl":"(//.+?)".*?"realName":"(.+?)",.*?"userId":(.*?),"'
		pattern = re.compile(regex, re.S)
		items = re.findall(pattern, page)