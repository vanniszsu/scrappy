#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pika
import oss2
import requests
import json

amqp_url = 'amqp://ptdmvfkd:tE5EEv5hSbYJeFcEQpIKT7WMuuZueGN0@black-boar.rmq.cloudamqp.com/ptdmvfkd'
queue = 'raw-image'
process_queue = 'image'

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
	data = json.loads(body)
	img = requests.get(data['url'])
	if img.status_code == 200:
		result = bucket.put_object(data['filename'], img)
		if result.status == 200:
			ch.basic_ack(delivery_tag = method.delivery_tag)
			if int(img.headers['Content-Length'])/1024/1024 > 1:
				ch.queue_declare(process_queue)
				ch.basic_publish(exchange='',
								 routing_key=process_queue
								 body=data['filename'])
			print "uploaded " + data['filename']
		else:
			print "Cannot upload" + data['filename']
	else:
		print "Cannot download the image " + data['filename']
		
connection = pika.BlockingConnection(pika.URLParameters(amqp_url))
channel = connection.channel()
channel.queue_declare(queue=queue)
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,queue=queue)

channel.start_consuming()