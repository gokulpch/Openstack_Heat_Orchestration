#!/usr/bin/env python

#AUTHOR: SAVITHRU LOKANATH
#CONTACT: SAVITHRU AT JUNIPER.NET

import sys
from vnc_api import vnc_api

def create_VirtualMachineInterface(vn, network_name, vnc, project, j):

	vn_obj = vnc_api.VirtualMachineInterface(name=network_name + str(j), parent_obj=project)
	vn_obj.add_virtual_network(vn)
	vnc.virtual_machine_interface_create(vn_obj)

        print 'VM "{}" created successfully\n'.format(network_name+str(j))

def create_VirtualNetwork(network_name, network_subnet, network_mask, vnc, project, i):

        """ FUNCTION TO CREATE VIRTUAL-NETWORK """

        vn_obj = vnc_api.VirtualNetwork(name=network_name, parent_obj=project)
        vn_obj.add_network_ipam(vnc_api.NetworkIpam(),
                        vnc_api.VnSubnetsType([vnc_api.IpamSubnetType(subnet = vnc_api.SubnetType(network_subnet,network_mask))]))

        vnc.virtual_network_create(vn_obj)

        print 'Network "{}" created successfully\n'.format(network_name)

	for j in range(1,254):
		create_VirtualMachineInterface(vn_obj, network_name + str(j), vnc, project, j)

def main():

        """ MAIN/AUTHENTICATE """

        vnc = vnc_api.VncApi(username='admin', password='contrail123', api_server_host = '10.84.18.11', tenant_name='admin')
        project = vnc.project_read(fq_name = ['default-domain', 'admin'])

        network_name = 'network'
        network_subnet = '192.168.100.'
        network_mask = 24

        for i in range(201,240):
		create_VirtualNetwork(network_name + str(i), network_subnet + str(i), network_mask, vnc, project, i)

if __name__=="__main__":
        main()
