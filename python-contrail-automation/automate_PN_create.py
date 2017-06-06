#!/usr/local/bin/python2.7

#Program to Automate Public-Net Creation
#Contact: slokanath at juniper dot net

import sys, os, argparse, yaml
from shutil import copyfile
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

def pushParams(prefix, route_target, hot_file, env_file, stack_name):

	""" FUNCTION TO CREATE HEAT STACK """

	prefix, prefix_len = prefix.split("/", 1)
	default_gw_list = prefix.split(".")
        default_gw_list[-1] = "1"
	default_gw = '.'.join(default_gw_list)
	
	env_file_bak = env_file + ".bak.env"

	if os.path.isfile(env_file):
		copyfile(env_file, env_file_bak)
		os.system("sed -i 's/{1}/" + prefix + "/g; s/{2}/" + prefix_len + "/g; s/{3}/" + default_gw + "/g; s/{4}/" + route_target + "/g' " + env_file_bak)
		os.system("heat stack-create " + stack_name + " -f " + hot_file + " -e " + env_file_bak)
	else:
		print "ENV file is not present/Path wrong"		
	
def getPrefix(routetbl, peer_logical):

	""" FUNCTION TO GET THE PREFIX """

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

	parser = argparse.ArgumentParser(add_help=True)

	parser.add_argument("-n", action="store",
                            help="Specify stack name")
	parser.add_argument("-v", action="store",
        	            help="Specify VRF")
	parser.add_argument("-f", action="store",
        	            help="Specify YAML/HOT file")
	parser.add_argument("-e", action="store",
        	            help="Specify ENV file")


	args = parser.parse_args()

	if args.n:
		stack_name = args.n
	if args.v:
		routing_instance_name = args.v
	if args.f:
		hot_file = args.f
	if args.e:
		env_file = args.e

	dev = Device(host='10.84.18.253', user='root', password='c0ntrail123').open()
	vrftbl = VRF(dev).get(values=True)
	iftbl = InterfaceTable(dev).get()
	routetbl = RouteTable(dev).get(protocol="static")
       	
	interface, route_target = routingInstance(vrftbl, routing_instance_name)
	peer_logical = peerUnit(iftbl, interface)
	prefix = getPrefix(routetbl, peer_logical)
	pushParams(prefix, route_target, hot_file, env_file, stack_name)
	dev.close()

#	except:
#		parser.print_help()
#		sys.exit(0)
        
if __name__=="__main__":
	main()
