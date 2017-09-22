#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika
import oss2

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

def callback(ch, method, properties, body):
	oss = Oss2bucket()
	bucket = oss.bucket