import os
from vnc_api import vnc_api

def scale_BGP(vnc, project_obj):

	""" SCALE BGPaaS """
	
	autonomous_system = "64512"
	bgpaas_attr = ["inet","inet6"]
	name = "bgp-"

	for i in range(1,1501):
		bgp_obj = vnc_api.BgpAsAService(name=name + str(i), parent_obj=project_obj, autonomous_system=autonomous_system, bgpaas_session_attributes={"address_families": {"family": bgpaas_attr }})
		uuid = vnc.bgp_as_a_service_create(bgp_obj)

		print "Successfully created BGPaaS {0} with UUID {1}\n".format(name + str(i), str(uuid))

def main():

	""" INIT FUNCTION """

	try:
		username = os.environ.get('OS_USERNAME')
        password = os.environ.get('OS_PASSWORD')
        project = os.environ.get('OS_TENANT_NAME')
        api_server = '10.87.121.101'

		vnc = vnc_api.VncApi(username=username, password=password, api_server_host = api_server, tenant_name=project)
		project_obj = vnc.project_read(fq_name = ['default-domain', project])
		scale_BGP(vnc, project_obj)

	except:
		print '\nERROR: Please source openstackrc file\n'

if __name__=="__main__":
	main()
