#! /usr/bin/python

from Modulos_ONOS import Request_REST_ONOS
from Modulos_ONOS import kafka_integration
import json


# se instancia la clase y crea el objeto request
request = Request_REST_ONOS('localhost', 'onos', 'rocks')
"""se hace una peticion GET a ONOS para traer la informacion de todos lo 
dispositivos y se guarda en deviceName solo los nombres de los dispositivos""" 
devicesName = request.get_DevicesName(request.GET_REST('devices'))


#se configuran los parametros relevantes de la regla de flujo a instanciar
#------------------------------------------------------------------------------
request.FLowRule['flows'][0]['priority'] = 5  #prioridad de la regla
request.FLowRule['flows'][0]['deviceId'] = devicesName['01'] #dispositivo en donde se instanciará la regla
request.FLowRule['flows'][0]['treatment']['instructions'] = [  #accion despues de haber match
				  {
		            'type': 'OUTPUT',
		            'port': '2'
		          }
		        ]
request.FLowRule['flows'][0]['selector']['criteria'] = [ #condiciones de match
          {
			'type': 'IN_PORT',
			'port': '1'
		  },
		  {
			'type': 'ETH_DST',
			'mac': '00:00:00:00:00:03'
		  },
		  {
			'type': 'ETH_SRC',
			'mac': '00:00:00:00:00:02'
		  }
        ]
#-----------------------------------------------------------------------------

#se envía la regla de flujo
respuesta = request.POST_REST('flows', request.FLowRule)

print('respuesta post: ', respuesta, '\n')

FlowRulesByDevice = request.get_FlowRulesByDevice(request.GET_REST('flows'), devicesName['01'])

print(FlowRulesByDevice)


