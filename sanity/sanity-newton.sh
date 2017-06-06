#!/bin/bash

wget https://launchpad.net/cirros/trunk/0.3.0/+download/cirros-0.3.0-x86_64-disk.img
openstack image create cirros --disk-format qcow2 --public --container-format bare --file cirros-0.3.0-x86_64-disk.img
openstack network create test-network
openstack  subnet create --subnet-range 192.168.1.0/24 --network test-network test-subnet
openstack flavor create --ram 512 --disk 1 --vcpus 1 m1.tiny

NET_ID=`neutron net-list | grep testvn | awk -F '|' '{print $2}' | tr -d ' '`e
openstack server create --flavor m1.tiny --image cirros --nic net-id=${NET_ID} test_vm1
openstack server create --flavor m1.tiny --image cirros --nic net-id=${NET_ID} test_vm2

openstack server list
