#!/bin/bash

cd ~/ && source openrc
wget http://10.84.5.120/cs-shared//images/ubuntu.img.gz
gunzip ubuntu.img.gz
glance image-create --name ubuntu --visibility=public --container-format ovf --disk-format qcow2 --file ubuntu.img
wget http://10.84.5.120/cs-shared//images/vsrx/junos-vsrx-12.1-in-network.img.gz
gunzip junos-vsrx-12.1-in-network.img.gz
glance image-create --name nat-service --visibility=public --container-format ovf --disk-format qcow2 --file junos-vsrx-12.1-in-network.img
git clone https://github.com/savithruml/HOT-OpenStack
heat stack-create sanity-check-sc -f /root/HOT-OpenStack/templates/nat-svc-stack-v2.hot -e /root/HOT-OpenStack/env/nat-svc-stack-v2.env

until heat stack-list | grep -i "complete" &> /dev/null; do sleep 2 ; done; echo "TEST PASS"
