
import os, paramiko
from opencsp.envmanagers.DefaultEnvManager.DefaultEnvManager import DefaultEnvManager
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo, ControlCheckBox
from fabric.api import *
from opencsp.envmanagers.EnvManager import EnvManager
from fabric.contrib.files import exists
from django.conf import settings

class RenartSpikeEnvManager(DefaultEnvManager):


	def turnon_server(self, server):
		"Turn the computer on"
		pass

	def remote_script(self, job):
		params = ' '.join( job.consoleparameters)
		appPath = os.path.join( '..',"applications", job.job_application.lower(), job.job_application+'.py' )
		
		command = 'source activate klusta \n'
		command += 'sudo /sbin/sysctl -w vm.drop_caches=3\n'
		command += 'PATH=$PATH:/home/csp/software/miniconda/envs/klusta/bin/\n'
		command += "python {0} {1} --exec execute >output.txt 2>&1\n".format(appPath, params)
		command += "mv busy.yes busy.no >>output.txt 2>&1\n"
		command += "sh ../stop.sh >>output.txt 2>&1\n"

		return command