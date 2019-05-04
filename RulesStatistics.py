from Modulos_ONOS import Request_REST_ONOS
from Modulos_ONOS import kafka_integration
import threading
import time
import os
import sys


if len(sys.argv) != 2:
	    print ("Usage: RulesStatistics.py IP_Controller    -   falta el parametro IP_Controller al ejecutar")
	    sys.exit(1)


request = Request_REST_ONOS(sys.argv[1], 'onos', 'rocks')
devicesName = request.get_DevicesName(request.GET_REST('devices'))


while 1 == 1:
	os.system('clear')
	print('\n //////////////////// # Rules by Device //////////////////// \n')
	Flows = request.GET_REST('flows')
	
	for d in devicesName:
		Nrules = len(request.get_FlowRulesByDevice(Flows, devicesName[d]))
		print(devicesName[d],' = ',Nrules,' Reglas ')
	print('\n ///////////////////////////////////////////////////////////')
	time.sleep(2)
