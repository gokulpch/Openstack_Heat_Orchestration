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


def create_ServiceTemplate(vnc):

        """ FUNCTION TO CREATE SERVICE-TEMPLATE """

        service_nat_template = 'service_nat_template'

        template = vnc_api.ServiceTemplate(name = service_nat_template)

        template_properties = vnc_api.ServiceTemplateType(
                        service_mode = 'in-network-nat',
                        service_type = 'firewall',
                        image_name = 'nat-service',
                        service_scaling = True,
			availability_zone = True)

        template_properties.add_interface_type(
                        vnc_api.ServiceTemplateInterfaceType(service_interface_type = 'management', shared_ip = False))
        template_properties.add_interface_type(
                        vnc_api.ServiceTemplateInterfaceType(service_interface_type = 'left', shared_ip = False))
        template_properties.add_interface_type(
                        vnc_api.ServiceTemplateInterfaceType(service_interface_type = 'right', shared_ip = False))

        template.set_service_template_properties(template_properties)

        vnc.service_template_create(template)

        print 'Service template "{}" created successfully\n'.format(service_nat_template)
        return template


def create_ServiceInstance(vnc, project, service_template):

        """ FUNCTION TO CREATE SERVICE-INSTANCE """

        instance = vnc_api.ServiceInstance(name = 'service_nat_instance', parent_obj=project)
        instance_properties = vnc_api.ServiceInstanceType(
                        scale_out = vnc_api.ServiceScaleOutType())

        instance.set_service_instance_properties(instance_properties)
        instance.set_service_template(service_template)

        vnc.service_instance_create(instance)


def main():

        """ MAIN/AUTHENTICATE """

        vnc = vnc_api.VncApi(username='admin', password='', api_server_host = '192.168.1.1', tenant_name='admin')
        project = vnc.project_read(fq_name = ['default-domain', 'admin'])

        left_network_name = 'left_VN'
        left_network_subnet = '192.168.200.0'
        left_network_mask = 24

        right_network_name = 'right_VN'
        right_network_subnet = '192.168.201.0'
        right_network_mask = 24

        create_VirtualNetwork(left_network_name, left_network_subnet, left_network_mask, vnc, project)
        create_VirtualNetwork(right_network_name, right_network_subnet, right_network_mask, vnc, project)

        service_template = create_ServiceTemplate(vnc)

        create_ServiceInstance(vnc, project, service_template)

if __name__=="__main__":
        main()