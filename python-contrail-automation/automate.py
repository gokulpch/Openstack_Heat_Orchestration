#!/usr/local/bin/python2.7

import sys
import yaml
from jnpr.junos import Device
from jnpr.junos.op.routes import RouteTable
from jnpr.junos.op.ethport import EthPortTable
from jnpr.junos.factory.factory_loader import FactoryLoader

YamlTable = \
    """
    VRF:
      get: routing-instances/instance
      args_key: name
      view: VRFView

    InterfaceTable:
      get: interfaces/interface
      view: InterfaceView

    VRFView:
      fields:
        instance_name: name
        instance_type: instance-type
        rd_type: route-distinguisher/rd-type
        vrf_target: vrf-target/community
        interface: interface/name

    InterfaceView:
      fields:
        name:       name
        unit:       unit/name
        peer:       unit/peer-unit
    """

globals().update(FactoryLoader().load(yaml.load(YamlTable)))

def getPrefix(routetbl, peer_logical):

	""" FUNCTION TO GET PREFIX """

	for route in routetbl:
		if route.via == peer_logical:
			return route.name
		else:
			pass

def peerUnit(iftbl, interface):

	""" FUNCTION TO GET THE PEER UNIT """

	interface_name, unit_number = interface.split(".", 1)

	for i in iftbl:
                if interface_name == i.name:
                        if unit_number in i.unit:
                                unit_match = i.unit.index(unit_number)
                                return interface_name + "." + i.peer[unit_match]
			else:
				print "Unit number did not match"
		else:
			print "Interface did not match"	

def routingInstance(vrftbl, routing_instance_name):

	""" FUNCTION TO GET THE ROUTE TARGET/INTERFACE """

	find = vrftbl[routing_instance_name]
        interface = [interface for interface in find.interface if interface.startswith('lt')][0]
	route_target = find.vrf_target

        return interface, route_target

def main():

	""" FUNCTION TO PERFORM INIT """

	try:
		dev = Device(host='', user='', password='').open()
        	vrftbl = VRF(dev).get(values=True)
		iftbl = InterfaceTable(dev).get()
		routetbl = RouteTable(dev).get(protocol="static")

        	routing_instance_name = str(sys.argv[1])

        	interface, route_target = routingInstance(vrftbl, routing_instance_name)
		peer_logical = peerUnit(iftbl, interface)
		prefix = getPrefix(routetbl, peer_logical)

		print route_target, prefix

	except:
		print "No Info found/Cannot connect"

        
if __name__=="__main__":
	main()
