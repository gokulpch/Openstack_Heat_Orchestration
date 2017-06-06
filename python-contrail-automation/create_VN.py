#!/usr/bin/env python

#AUTHOR: SAVITHRU LOKANATH
#CONTACT: SAVITHRU AT JUNIPER.NET

import sys
from vnc_api import vnc_api


def create_VirtualNetwork(network_name, network_subnet, network_mask, vnc, project):

        """ FUNCTION TO CREATE VIRTUAL-NETWORK """

        vn_obj = vnc_api.VirtualNetwork(name=network_name, parent_obj=project)
        vn_obj.add_network_ipam(vnc_api.NetworkIpam(),
                        vnc_api.VnSubnetsType([vnc_api.IpamSubnetType(subnet = vnc_api.SubnetType(network_subnet,network_mask))]))

        vnc.virtual_network_create(vn_obj)

        print 'Network "{}" created successfully\n'.format(network_name)


def main():

        """ MAIN/AUTHENTICATE """

        vnc = vnc_api.VncApi(username='admin', password='', api_server_host = '192.168.1.1', tenant_name='admin')
        project = vnc.project_read(fq_name = ['default-domain', 'admin'])

        left_network_name = 'left_VN'
        left_network_subnet = '192.168.200.0'
        left_network_mask = 24

        create_VirtualNetwork(left_network_name, left_network_subnet, left_network_mask, vnc, project)

if __name__=="__main__":
        main()
