#! /usr/bin/python

from Modulos_ONOS import Request_REST_ONOS
from Modulos_ONOS import kafka_integration
from bottle import Bottle, run, request
import threading
import json



app = Bottle()


@app.route('/hello', method='GET')
def hello():
    return "Hello World!"


@app.route('/alarma', method='POST')
def alarma():
	global alarmas
	r = json.load(request.body)
	IPdest,IPsource,PortS,PortD = r['claves'].split(",")
	print('\n Alerta:')
	print('IPdest:',IPdest,' IPsource:',IPsource,' PortS:',PortS, ' PortD:', PortD)
	Accion(IPdest,IPsource,PortS,PortD)
	print('-------------------------------')



def Accion(IPdest,IPsource,PortS,PortD):
	request = Request_REST_ONOS('localhost', 'onos', 'rocks')
	devicesName = request.get_DevicesName(request.GET_REST('devices'))

	#se configuran los parametros relevantes de la regla de flujo a instanciar
	#------------------------------------------------------------------------------
	request.FLowRule['flows'][0]['priority'] = 50000  #prioridad de la regla
	request.FLowRule['flows'][0]['isPermanent'] = 'false'
	request.FLowRule['flows'][0]['timeout'] = 10
	request.FLowRule['flows'][0]['treatment']['instructions'] = []  #accion despues de haber match
	request.FLowRule['flows'][0]['selector']['criteria'] = [ #condiciones de match
			      {
			        "type": "ETH_TYPE",
			        "ethType": "0x0800"
			      },
			      {
			        "type": "IP_PROTO",
			        "protocol": 6
			      },
			      {
			        "type": "IPV4_SRC",
			        "ip": IPsource + '/8'
			      },
			      {
			        "type": "IPV4_DST",
			        "ip": IPdest + '/8'
			      },
			      {
			        "type": "TCP_SRC",
			        "tcpPort": PortS
			      },
			      {
			        "type": "TCP_DST",
			        "tcpPort": PortD
			      }
	        ]
	#-----------------------------------------------------------------------------
	for x in devicesName:
		request.FLowRule['flows'][0]['deviceId'] = devicesName[x]
		print(request.POST_REST('flows', request.FLowRule))



if __name__ == '__main__':
	try:
	    app.run(host='0.0.0.0', port=5000)
	except BaseException as e:
	    log.error(e.message)
