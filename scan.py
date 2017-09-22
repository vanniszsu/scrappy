#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import oss2
import requests
import sys
import pika
import json

amqp_url = 'amqp://ptdmvfkd:tE5EEv5hSbYJeFcEQpIKT7WMuuZueGN0@black-boar.rmq.cloudamqp.com/ptdmvfkd'
queue = 'raw-image'
		
class Oss2bucket:
	def __init__(self, bucketname=None):
		self.__AK = "/etc/ossAK"
		self.__endpoint = "oss-cn-shanghai.aliyuncs.com"
		self.__bucketname = "scrapy-images"
		if bucketname == None:
			bucketname = self.__bucketname
		access = ((open(self.__AK)).read()).split(',')
		self.__auth = oss2.Auth(access[0],access[1])
		self.bucket = oss2.Bucket(self.__auth, self.__endpoint, bucketname)
			

class Spider:
	def __init__(self):
		self.siteURL = "https://mm.taobao.com/tstar/search/tstar_model.do"
		
	def getPage(self,pageindex):
		payload = {'_input_charset':'utf-8','currentPage':pageindex}
		page = requests.post(self.siteURL, params=payload)
		if page.status_code == 200:
			return page.text
		else:
			sys.exit("Cannot get the web page")
			
	def getAllimages(self,pageindex):
		page = self.getPage(pageindex)
		regex = '"cardUrl":"(//.+?)".*?"realName":"(.+?)",.*?"userId":(.*?),"'
		pattern = re.compile(regex, re.S)
		items = re.findall(pattern, page)
		return items
	
	def addimages(self,number,start_page=1):
		count = 0
		pageindex = start_page
		oss = Oss2bucket()
		bucket = oss.bucket
		while count < number:
			items = self.getAllimages(pageindex)
			for item in items:
				imageURL = "https:" + item[0]
				filename = item[1] + '-' + item[2] + ".jpg"
				if not(bucket.object_exists(filename)):
					data = {"url":imageURL, "filename":filename}
					message = json.dumps(data)
					connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
					channel = connection.channel()
					channel.basic_publish(exchange='',
										  routing_key=queue,
										  
					if img.status_code == 200:
						result = bucket.put_object(filename, img)
						if result.status == 200:
							count += 1
							if int(img.headers['Content-Length'])/1024/1024 > 1:
								rbmq.pushm(filename)
							if count >= number:
								break
						else:
							print "Cannot save " + filename + " to Aliyun OSS"
					else:
						print "Cannot download the image " + filename
			pageindex += 1
			
