#! /usr/bin/python

from Modulos_ONOS import Request_REST_ONOS
from Modulos_ONOS import kafka_integration
import json


conexion = kafka_integration('localhost','onos','rocks','EventosKafka')
conexion.register()
conexion.subscribe('DEVICE')
conexion.consume()
