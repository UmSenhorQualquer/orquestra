import os, paramiko
from opencsp.envmanagers.LIPEnvManager.LIPEnvManager import LIPEnvManager
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo, ControlCheckBox

from fabric.api import *
from fabric.contrib.files import exists
from django.conf import settings
from opencsp.envmanagers.DefaultEnvManager.fabproject import rsync_project


class LIPHPCEnvManager(LIPEnvManager):

	def __init__(self): super(LIPHPCEnvManager, self).__init__()

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

	def turnon_server(self, server):
		"Turn the computer on"
		pass

	def setup_application(self, server, application):
		"""
		Setup the node environment in the remote server
		"""
		self.initCredentials(server)
		
		local_dir  = os.path.join(settings.PYFORMS_APPLICATIONS_PATH,application.algorithm_class.lower() )
		remote_dir = os.path.join(self._base_dir,'applications' )
	
		rsync_project(
			local_dir = local_dir,
			remote_dir= remote_dir,
			exclude=('.svn','*.pyc','output','ants'),
			delete=True,
			sshpass=True
		)

		server.run( """echo "PYFORMS_MODE = 'TERMINAL'" >> {0}""".format( os.path.join(remote_dir, application.algorithm_class.lower(),'settings.py') ))
		

	def remote_script(self, job):
		params = ' '.join( job.consoleparameters)
		appPath = os.path.join('$OPENCSP_HOME',"applications", job.job_application.lower(), job.job_application+'.py' )
		
		command = """#!/bin/bash
			#######
			# HPC #
			#######
			#$ -pe mp 1
			#$ -q hpcgrid
			#$ -P HpcGrid
			#$ -l infiniband=y
			#$ -cwd

			#$ -j yes
			#$ -o output.txt

			module load gcc-4.6.3
			module load opencsp-1.0

			mkdir output
			python {0} {1} --exec execute 
			echo {2} > busy.no
			""".format( appPath, params, str(job.pk)  ).replace('\t\t\t','')

		return command