#!/usr/bin/env python

import sys, os
from shutil import copyfile

def process():

list_ip_1 = ["192.168.1.1", "192.168.1.2", "192.168.1.3"]
list_ip_2 = ["192.168.2.1", "192.168.2.2", "192.168.2.3"]

for i in list_ip_1:
	tmp_file = i + "_ip.json"
	copyfile("template.json", tmp_file)
	for j in list_ip_2:
		os.system("sed -i -r 's/{1}/" + i + "/g; s/{2}/" + j +  "/g' " + tmp_file)
		

def main():
	process()

if __name__ == '__main__':
    sys.exit(main())
