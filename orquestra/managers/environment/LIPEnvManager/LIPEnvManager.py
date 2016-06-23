import os, paramiko
from opencsp.envmanagers.DefaultEnvManager.DefaultEnvManager import DefaultEnvManager
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo, ControlCheckBox
from fabric.api import *
from fabric.contrib.files import exists
from django.conf import settings
from opencsp.envmanagers.DefaultEnvManager.fabproject import rsync_project

class LIPEnvManager(DefaultEnvManager):

	_base_dir = '/exper-sw/neuro/opencsp'

	

	def initCredentials(self, server):
		env.host_string = server.host_string
		env.disable_known_hosts = True

	def put(self, server, origin, destiny): 
		self.initCredentials(server)
		run(	"mkdir 	-p %s    " % destiny 	)
		put( origin, destiny)

	def turnon_server(self, server):
		"Turn the computer on"
		pass

	def server_jobinfo(self, job):
		server = job.server
		self.initCredentials(server)
		out = ''
		
		try:
			out += str(run("qstat | grep opencsp"))			
		except:
			out += 'Error on calling top'
		
		try:
			out += "\n\n----------------------------------------------------------------------------"
			out += "\n\n" + str( run("ls -R -lh {0}".format( os.path.join(server.running_env, 'output') ) ) )
		except:
			out += '\n\nError happend, on checking the output folder'

		return out

	def setup_node(self, server):
		"""
		Setup common features to several nodes in the same remote server
		"""
		self.initCredentials(server)
		#Creates the remote server directory
		server.run("mkdir 	-p %s    " % server.running_env )

		print 'Setup node in server', str(server)

		#Sync the slave environment
		local_dir  = os.path.join(settings.BASE_DIR,'slave','framework','*')
		remote_dir = os.path.join(self._base_dir,'framework')

		rsync_project(
			local_dir = local_dir,
			remote_dir= remote_dir,
			exclude=('.svn','*.pyc','applications'),
			delete=True,
			sshpass=True
		)

	
	def setup_application(self, server, application):
		"""
		Setup the node environment in the remote server
		"""
		self.initCredentials(server)
		#Synchronize the application attributed to this server

		local_dir  = os.path.join(settings.BASE_DIR,'applications',application.algorithm_class.lower() )
		remote_dir = os.path.join(self._base_dir,'applications' )
	
		rsync_project(
			local_dir = local_dir,
			remote_dir= remote_dir,
			exclude=('.svn','*.pyc','output'),
			delete=True,
			sshpass=True
		)


	def run_job(self, job): job.server.paramikoRun( 'cd %s; qsub run.sh' % job.server.running_env )


	def remote_script(self, job):
		params = ' '.join( job.consoleparameters)
		appPath = os.path.join('$OPENCSP_HOME',"applications", job.job_application.lower(), job.job_application+'.py' )
		
		command = """#!/bin/bash
			#$ -v SGEIN1=input
			#$ -v SGEIN2=server_id.txt
			#$ -v SGEOUT1=output
			#$ -v SGEOUT2=busy.no

			#$ -j yes
			#$ -o output.txt

			module load opencsp-1.0

			mkdir output
			echo {2} > busy.no
			python {0} {1} --exec execute 
			""".format( appPath, params, str(job.pk) ).replace('\t\t\t','')

		return command

