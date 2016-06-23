import os, paramiko
from opencsp.envmanagers.LIPHPCEnvManager.LIPHPCEnvManager import LIPHPCEnvManager
from pyforms.Controls import ControlSlider
from pyforms.Controls import ControlFile
from pyforms.Controls import ControlText
from pyforms.Controls import ControlCombo
from fabric.api import *
from fabric.contrib.files import exists
from django.conf import settings


class LIPHPCEnvManagerAppSpikeSorter(LIPHPCEnvManager):

	def __init__(self):  super(LIPHPCEnvManagerAppSpikeSorter, self).__init__()

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

	def close_setup_node(self, server, application):
		server.run('rsync -av /exper-sw/neuro/opencsp/framework/pyforms /exper-sw/neuro/miniconda/envs/klusta/lib/python2.7/site-packages/')

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

			source /exper-sw/neuro/miniconda/bin/activate klusta
			OPENCSP_HOME=/exper-sw/neuro/opencsp
			PATH=$PATH:/exper-sw/neuro/miniconda/bin:/exper-sw/neuro/opencsp/framework
			
			mkdir output
			python {0} {1} --exec execute 
			echo {2} > busy.no
			""".format( appPath, params, job.pk ).replace('\t\t\t','')

		return command


