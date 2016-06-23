import os, paramiko
from opencsp.envmanagers.LIPEnvManager.LIPEnvManager import LIPEnvManager
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo, ControlCheckBox
from fabric.api import *
from fabric.contrib.files import exists
from django.conf import settings

class LIPEnvManagerAppSpikeSorter(LIPEnvManager):

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

			source /exper-sw/neuro/miniconda/bin/activate klusta
			OPENCSP_HOME=/exper-sw/neuro/opencsp
			PATH=$PATH:/exper-sw/neuro/miniconda/bin:/exper-sw/neuro/opencsp/framework

			mkdir output
			echo {2} > busy.no
			python {0} {1}  --exec execute 

			source deactivate
			""".format( appPath, params, str(job.pk) ).replace('\t\t\t','')

		return command


