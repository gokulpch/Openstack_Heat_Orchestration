#!/usr/bin/env python

#AUTHOR: SAVITHRU LOKANATH
#CONTACT: SAVITHRU AT JUNIPER.NET

import sys, os, time, paramiko
from vnc_api import vnc_api
from novaclient.v2 import client

def wait():

	for i in range(21):
    		sys.stdout.write('\r')
    		sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
    		sys.stdout.flush()
    		time.sleep(1)

def test_Connectivity(host1, host2, username, password):

	""" FUNCTION TO TEST CONNECTIVITY """

	print "Checking connectivity\n"
	wait()
	print "\n"
	
	try:
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(host1, 22, username, password)
		cmd = 'ping -c 3 ' + host2 + '; echo $?'

		stdin, stdout, stderr = client.exec_command(cmd)
		out = stdout.readlines()[-1].strip()
		
		if str(out) == "0":
			print "Ping successful\n"
		else:
			print "Ping unsuccessful\n"

	except:
		pass	

def delete_Env(nova, vm_name_1, vm_name_2, policy_name, left_network_name, right_network_name, vnc, domain, project_name):

	""" FUNCTION TO DELETE THE ENVIRONMENT """

	project = vnc.project_read(fq_name = [domain, project_name])

	try:
                fip_list = open("fip_uuid.txt").read().strip().split("\n")
                for fip in fip_list:
			time.sleep(2)
                        nova.floating_ips.delete(fip)
                        print 'Floating IP {} deleted successfully\n'.format(fip)
			os.remove("fip_uuid.txt")

        except:
                pass

	vm_delete_list = [vm_name_1, vm_name_2]
	
	for vm in vm_delete_list:
		try:
			nova.servers.find(name=vm).delete()
			print 'Server "{}" deleted successfully\n'.format(vm)

		except:
			print 'Server "{}" does not exist\n'.format(vm)

	try:
		fip_list = open("fip_uuid.txt").read().strip().split("\n")
		for fip in fip_list:
			nova.floating_ips.delete(fip)
			print 'Floating IP {} successfully deleted\n'.format(fip_uuid)

        	os.remove("fip_uuid.txt")
	
	except:
		pass
	
	time.sleep(5)
	vn_delete_list = [left_network_name, right_network_name]

	for vn in vn_delete_list:
		try:	
			vnc.virtual_network_delete(fq_name= [domain, project_name, vn])
			print 'Virtual Network "{}" deleted successfully\n'.format(vn)

		except:
			print 'Virtual Network "{}" does not exist\n'.format(vn)
 
	try:
		vnc.network_policy_delete(fq_name= [domain, project_name, policy_name])
		print 'Network Policy "{}" deleted successfully\n'.format(policy_name)
	
	except:
		print 'Network Policy "{}" does not exist\n'.format(policy_name)
	

def launch_VM(nova, project_name, vm_name, image_name, flavor_type, network):

	""" FUNCTION TO LAUNCH A VIRTUAL MACHINE """

        image = nova.images.find(name = image_name)
        flavor = nova.flavors.find(name = flavor_type)
        network = nova.networks.find(label = network)
      	nova.floating_ip_pools.list()
        floating_ip = nova.floating_ips.create(nova.floating_ip_pools.list()[0].name)
        nova.servers.create(name=vm_name, image=image.id, flavor=flavor.id, nics=[{'net-id': network.id}])
	
	os.system('echo ' + floating_ip.id + ' >> fip_uuid.txt')
	
        print 'Server "{}" created successfully\n'.format(vm_name)        

        time.sleep(2)
	nova.servers.find(name=vm_name).add_floating_ip(floating_ip)

        print 'Floating IP "{}" attached to "{}"\n'.format(floating_ip.ip, vm_name)

	return floating_ip.ip

def create_NetworkPolicy(policy_name, left_network_name, right_network_name, vnc, domain, project_name):

	""" FUNCTION TO CREATE NETWORK POLICY """

        project = vnc.project_read(fq_name = [domain, project_name])

        rule = vnc_api.PolicyRuleType(direction = '<>', protocol = 'any',
                action_list = vnc_api.ActionListType(simple_action = 'pass'),
                src_addresses = [vnc_api.AddressType(virtual_network = left_network_name)],
                src_ports = [vnc_api.PortType(start_port = -1, end_port = -1)],
                dst_addresses = [vnc_api.AddressType(virtual_network = right_network_name)],
                dst_ports = [vnc_api.PortType(start_port = -1, end_port = -1)])
        policy = vnc_api.NetworkPolicy(name = policy_name, parent_obj = project, network_policy_entries = vnc_api.PolicyEntriesType([rule]))
        
        vnc.network_policy_create(policy)

        print 'Policy "{}" created between "{}" & "{}"\n'.format(policy_name, left_network_name, right_network_name)

def add_NetworkPolicy(policy_name, network, vnc, domain, project_name):

	""" FUNCTION TO ATTACH NETWORK POLICY TO VIRTUAL_NETWORKS """

        policy = vnc.network_policy_read(fq_name = [domain, project_name, policy_name])

        policy_type = vnc_api.VirtualNetworkPolicyType(sequence = vnc_api.SequenceType(major = 0, minor = 0))
        vn = vnc.virtual_network_read(fq_name = [domain, project_name, network])
        vn.add_network_policy(ref_obj = policy, ref_data = policy_type)
        
        vnc.virtual_network_update(vn)

        print 'Policy "{}" attached to "{}"\n'.format(policy_name, network)


def create_VirtualNetwork(network_name, network_subnet, network_mask, network_gateway, vnc, domain, project_name):

        """ FUNCTION TO CREATE VIRTUAL-NETWORK """

        project = vnc.project_read(fq_name = [domain, project_name])

        vn_obj = vnc_api.VirtualNetwork(name=network_name, parent_obj=project)
        vn_obj.add_network_ipam(vnc_api.NetworkIpam(),
                        vnc_api.VnSubnetsType([vnc_api.IpamSubnetType(subnet = vnc_api.SubnetType(network_subnet,network_mask), default_gateway = network_gateway)]))

        vnc.virtual_network_create(vn_obj)

        print 'Network "{}" created successfully\n'.format(network_name)

def main():

        """ MAIN/AUTHENTICATE """

        project_name = 'admin'
        domain = 'default-domain'
        username = 'admin'
        password = 'xyz123'
        api_server = '10.84.18.1'
        auth_url = "http://10.84.18.1:5000/v2.0/"

        left_network_name = 'left_VN'
        left_network_subnet = '1.1.1.0'
        left_network_mask = 24
        left_network_gateway = '1.1.1.1'

        right_network_name = 'right_VN'
        right_network_subnet = '2.2.2.0'
        right_network_mask = 24
        right_network_gateway = '2.2.2.1'

	vm_name_1 = "vm_1"
        vm_name_2 = "vm_2"
        image = "ubuntu"
        flavor = "m1.tiny"
	vm_username = "ubuntu"
	vm_password = "ubuntu"

        policy_name = 'red-to-blue'

	vnc = vnc_api.VncApi(username=username, password=password, api_server_host = api_server, tenant_name=project_name)
	nova = client.Client(username, password, project_name, auth_url, service_type="compute")
	
        if len(sys.argv) == 2 and (sys.argv[1]) == "-d":
        	delete_Env(nova, vm_name_1, vm_name_2, policy_name, left_network_name, right_network_name, vnc, domain, project_name)

	elif len(sys.argv) == 2 and (sys.argv[1]) == "-c":
	        create_VirtualNetwork(left_network_name, left_network_subnet, left_network_mask, left_network_gateway, vnc, domain, project_name)
        	create_VirtualNetwork(right_network_name, right_network_subnet, right_network_mask, right_network_gateway, vnc, domain, project_name)

        	create_NetworkPolicy(policy_name, left_network_name, right_network_name, vnc, domain, project_name)
        	add_NetworkPolicy(policy_name, left_network_name, vnc, domain, project_name)
        	add_NetworkPolicy(policy_name, right_network_name, vnc, domain, project_name)

        	host1 = launch_VM(nova, project_name, vm_name=vm_name_1, image_name=image, flavor_type=flavor, network=left_network_name)
        	host2 = launch_VM(nova, project_name, vm_name=vm_name_2, image_name=image, flavor_type=flavor, network=right_network_name)
                time.sleep(30)
		test_Connectivity(host1, host2, vm_username, vm_password)
	
	else:
        	print "Invalid argument\n\nUSAGE:\n\nTo create environment: python <file.py> -c\nTo delete environment: python <file.py> -d\n"

if __name__=="__main__":
        main()
