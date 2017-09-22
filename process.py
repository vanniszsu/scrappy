#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika
import oss2
import requests
from math import ceil

amqp_url = 'amqp://ptdmvfkd:tE5EEv5hSbYJeFcEQpIKT7WMuuZueGN0@black-boar.rmq.cloudamqp.com/ptdmvfkd'
queue = 'image'

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
	oss = Oss2bucket('scrapy-images')
	bucket = oss.bucket
	url = bucket.sign_url('GET', body, 300, params={'x-oss-process':'image/info'})
	info = (requests.get(url)).json()
	size = int(info['FileSize']['value'])
	ratio = "{0:.0f}".format(1. / ceil(size/1024./1024.) * 2.5 * 100)
	style = 'image/resize,p_' + ratio
	url = bucket.sign_url('GET', body, 300, params={'x-oss-process':style})
	img = requests.get(url)
	result = bucket.put_object(body, img)
	if result.status == 200:
		ch.basic_ack(delivery_tag = method.delivery_tag)

connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
channel = connection.channel()
channel.queue_declare(queue=queue)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,queue=queue)

channel.start_consuming()