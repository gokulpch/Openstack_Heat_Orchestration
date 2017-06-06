#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Author: SAVITHRU LOKANATH
# Contact: SAVITHRU AT JUNIPER.NET
# Copyright (c) 2016 Juniper Networks, Inc. All rights reserved.

import os
import timeit
import argparse
from vnc_api import vnc_api


def update_SG(vnc, project, sg_old, sg_new, virtual_network):

	""" FUNCTION TO UPDATE SECURITY-GROUPS """

	try:
		if sg_old != sg_new:
			security_grp = vnc.security_group_read(fq_name=['default-domain', project, sg_new])	
			vmi_list = vnc.virtual_machine_interfaces_list()['virtual-machine-interfaces']

			for vmi in vmi_list:
				if vmi['fq_name'][1] == project and vmi['fq_name'][2].startswith(virtual_network + '-'):
					vmi_obj = vnc.virtual_machine_interface_read(vmi['fq_name'])
					sg_ref_old = vmi_obj.get_security_group_refs()[0]['to'][2]

					if sg_ref_old == sg_old:
						start_time = timeit.default_timer()
						vmi_obj.set_security_group(security_grp)
						vnc.virtual_machine_interface_update(vmi_obj)
						elapsed = timeit.default_timer() - start_time
						sg_ref_new = vmi_obj.get_security_group_refs()[0]['to'][2]
						print 'INFO: Security group on VMI "{}" updated from "{}" to "{}" in {} seconds'.format(vmi['fq_name'][2], sg_ref_old, sg_ref_new, elapsed)

					elif sg_ref_old == sg_new:
						print 'INFO: Security group "{}" on VMI "{}" already exists'.format(sg_ref_old, vmi['fq_name'][2])				

					else:
						pass

				else:
					pass

		else:
			print '\nERROR: Old & new security groups are the same\n'

	except:
		print '\nERROR: The security group does not exist\n'


def main():

	""" INIT FUNCTION """

	try:

		username = os.environ.get('OS_USERNAME')
        	password = os.environ.get('OS_PASSWORD')
        	api_server = os.environ.get('OS_AUTH_URL').split("//")[1].split(":")[0]
        	project = os.environ.get('OS_TENANT_NAME')

		parser = argparse.ArgumentParser()
		required = parser.add_argument_group('Required Arguments')
        	required.add_argument('--from', action='store', dest='old_sg', help='Old security-group name')
		required.add_argument('--to', action='store', dest='new_sg', help='New security-group name')
		required.add_argument('--vn', action='store', dest='vn', help='Virtual-Network')
        	args = parser.parse_args()

		if args.old_sg and args.new_sg and args.vn:
			sg_old, sg_new, virtual_network = args.old_sg, args.new_sg, args.vn
			vnc = vnc_api.VncApi(username=username, password=password, api_server_host = api_server, tenant_name=project)
			update_SG(vnc, project, sg_old, sg_new, virtual_network)
		else:
			parser.print_help()

	except:
		print '\nERROR: Please source openstackrc file\n'

if __name__=="__main__":

	start_time = timeit.default_timer()
	main()
	elapsed = timeit.default_timer() - start_time
	
	print '\nExecution Time: {}\n'.format(elapsed)
