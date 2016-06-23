from opencsp.envmanagers.DefaultEnvManager.DefaultEnvManager import DefaultEnvManager
from fabric.api import *
#import boto3, os, time

class AWSEnvManager(DefaultEnvManager):
	
	def initCredentials(self, server):
		env.host_string 	= server.host_string
		env.key_filename 	= server.server_certificate
		env.disable_known_hosts = True

		print env.host_string, env.key_filename

	#######################################################################################
	##### Node setup related ##############################################################
	#######################################################################################

	def setup_node(self, server): pass
	def setup_application(self, server, application): pass

	#######################################################################################
	##### Server info #####################################################################
	#######################################################################################

	def server_checkconnection(self, server): return False

	def turnon_server(self, server):
		ec2 = boto3.resource('ec2')
		new_instances = ec2.create_instances(
			ImageId			= 'ami-2c6bc45f',
			InstanceType	= 't2.micro', 
			KeyName 		= 'aws-mine',
			SecurityGroups	= ['default'],
			MinCount = 1,	MaxCount = 1)

		new_instance = new_instances[0]
		while True:
			instance = ec2.Instance(new_instance.id)
			if instance.state['Name']=='running':
				server.server_host = instance.public_dns_name
				out, error = server.paramikoRun('echo True')
				if out.startswith('True'): break
			time.sleep(1)
		time.sleep(10)

		server.server_host = instance.public_dns_name
		server.save()

		path = os.path.dirname(__file__)
		f = open( os.path.join(path, 'aws-instances', str(server.pk) + ".txt"), 'w' )
		f.write(instance.instance_id)
		f.close()



	def turnoff_server(self, server):

		server.server_host = None
		server.save()
		
		path = os.path.dirname(__file__)
		f = open( os.path.join(path, 'aws-instances', str(server.pk) + ".txt"), 'r' )
		instance_id = f.read(); f.close()

		ec2 	 = boto3.resource('ec2')
		instance = ec2.Instance(instance_id)
		instance.terminate()