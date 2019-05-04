#! /usr/bin/python

import requests
import json
import random
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from confluent_kafka import Producer


class Functionalities:

	def __init__(self):
		self.FLowRule = {
		  'flows': [
		    {
		      'priority': 40000,
		      'timeout': 0,
		      'isPermanent': 'true',
		      'deviceId': '',
		      'treatment': {
		        'instructions': []
		      },
		      'selector': {
		        'criteria': []
		      }
		    }
		  ]
		}
	

	def get_DevicesName(self, devices):
		devicesName = {}
		for x in devices['devices']:
			devicesName[str(x['id'][-2])+str(x['id'][-1])] = x['id']
		return devicesName


	def get_FlowRulesByDevice(self, Flows, device):
		FlowRulesByDevice = [] 
		for x in Flows['flows']:
			if x['deviceId'] == device:
				FlowRulesByDevice.append(x)
		return FlowRulesByDevice

	def randomMAC(self):
		lista = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
		MAC = random.choice(lista)+random.choice(lista)
		for x in range(1,6):
			MAC = MAC + ':'+random.choice(lista)+random.choice(lista)
		return MAC


class Request_REST_ONOS(Functionalities):

	def __init__(self, IPserver, user, password):
		Functionalities.__init__(self)
		self.url = 'http://'+IPserver+':8181/onos/v1/'
		self.user = user
		self.password = password


	def Validation_Response(self, reply):
		if reply.status_code == 200:
			return reply.json()
		elif reply.status_code == 404:
			return 'ERROR:' + str(reply.status_code) + ' - No se encontró la URL'
		elif reply.status_code == 401:
			return 'ERROR:' + str(reply.status_code) + ' - Autenticacion Fallida'
		elif reply.status_code == 405:
			return 'ERROR:' + str(reply.status_code) + ' - El destino no soporta la peticion'
		elif reply.status_code == 400:
			print('err:',reply.text)
			return 'ERROR:' + str(reply.status_code) + ' - Peticion mal formada, el servidor no puede procesarla'
		else:
			return 'ERROR:' + str(reply.status_code)


	def GET_REST(self, endpoint):
		rest = self.url + endpoint
		reply = requests.get(rest, auth=(self.user,self.password))

		return self.Validation_Response(reply)


	def POST_REST(self, endpoint, payload):
		rest = self.url + endpoint
		reply = requests.post(rest, data=json.dumps(payload), auth=(self.user, self.password))

		return self.Validation_Response(reply)


	def DELETE_REST(self,endpoint,payload):
		rest = self.url + endpoint
		reply = requests.delete(rest, data=json.dumps(payload), auth=(self.user, self.password))

		return self.Validation_Response(reply)


class kafka_integration:

	def __init__(self, IPserver, user, password, appName):
		self.url = 'http://'+IPserver+':8181/onos/kafka-integration/kafkaService'
		self.IPserver = IPserver
		self.user = user
		self.password = password
		self.appName = appName
		self.groupId = ''
		self.evento = ''


	def register(self):
		dst = self.url + '/register'
		response = requests.post(dst, data=self.appName, auth=(self.user, self.password))
		print('Registro de la aplicacion:\n',response.text)
		r = json.loads(response.text)
		self.groupId = r['groupId']


	def subscribe(self,evento):
		self.evento = evento
		dst = self.url + '/subscribe'
		payload = {
  			'appName': self.appName,
  			'groupId': self.groupId,
  			'eventType': self.evento
		}
		response = requests.post(dst, data=json.dumps(payload), auth=(self.user, self.password))
		print('\n Subscripcion al evento: \n',response.text)


	def consume(self):
		c = Consumer({
	    	'bootstrap.servers': self.IPserver,
	    	'group.id': self.groupId,
	    	'session.timeout.ms': 6000,
	    	'auto.offset.reset': 'earliest'
		})

		c.subscribe([self.evento])

		while True:
		    msg = c.poll(1.0)

		    if msg is None:
		        continue
		    if msg.error():
		        #print("Consumer error: {}".format(msg.error()))
		        continue

		    #print('Received message: {}'.format(msg.value()))
		    print('payload:',msg.value())
		    print('offset:'+str(msg.offset()))
		    print('partition:'+str(msg.partition()))
		    print('topic:'+str(msg.topic()),'\n\n')

		c.close()