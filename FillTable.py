from Modulos_ONOS import Request_REST_ONOS
import threading
import sys



def Fill():
	request = Request_REST_ONOS(sys.argv[1], 'onos', 'rocks')
	devicesName = request.get_DevicesName(request.GET_REST('devices'))

	#se configuran los parametros relevantes de la regla de flujo a instanciar
	#------------------------------------------------------------------------------
	request.FLowRule['flows'][0]['priority'] = 10  #prioridad de la regla
	request.FLowRule['flows'][0]['isPermanent'] = 'false'
	request.FLowRule['flows'][0]['timeout'] = 100
	request.FLowRule['flows'][0]['deviceId'] = devicesName['01'] #dispositivo en donde se instanciará la regla
	request.FLowRule['flows'][0]['treatment']['instructions'] = [  #accion despues de haber match
					  {
			            'type': 'OUTPUT',
			            'port': '2'
			          }
			        ]

	while 1 == 1:
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
				'mac': request.randomMAC()
			  }
	        ]

	    #se envía la regla de flujo
		respuesta = request.POST_REST('flows', request.FLowRule)
		print(respuesta)


if __name__ == '__main__':
	
	if len(sys.argv) != 2:
		print("Falta IP del controlador")
		sys.exit(1)
	
	t1 = threading.Thread(name="random1", target=Fill, args=())
	t2 = threading.Thread(name="random2", target=Fill, args=())
	t3 = threading.Thread(name="random3", target=Fill, args=())
	t4 = threading.Thread(name="random4", target=Fill, args=())

	t1.start()
	t2.start()
	t3.start()
	t4.start()
