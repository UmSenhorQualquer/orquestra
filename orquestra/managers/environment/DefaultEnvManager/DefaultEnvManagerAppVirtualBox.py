import os, paramiko, logging
from opencsp.envmanagers.DefaultEnvManager.DefaultEnvManager import DefaultEnvManager
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo, ControlCheckBox
from fabric.api import *
from fabric.contrib.files import exists
from django.conf import settings
from opencsp.envmanagers.DefaultEnvManager.fabproject import rsync_project


class DefaultEnvManagerAppVirtualBox(DefaultEnvManager):

	def __init__(self):  super(DefaultEnvManagerAppVirtualBox, self).__init__()

	def prepare_job(self, job):
		f = open('/var/www/phpvirtualbox/hosts/{0}.php'.format(job.pk), 'w')
		f.write("""<?php 
		return array(
			'name' => '{2}',
			'username' => '{0}',
			'password' => 'bugz111a',
			'location' => 'http://{1}:18083/',
			'authMaster' => true // Use this server for authentication
		  );
		?>""".format(job.server.server_user, job.server.server_host, job.server.server_name) )
		f.close()
		super(DefaultEnvManagerAppVirtualBox, self).prepare_job(job)
	

	def kill(self, job):
		logging.debug( "DefaultEnvManagerAppVirtualBox::kill({0})".format(job) )
		os.remove('/var/www/phpvirtualbox/hosts/{0}.php'.format(job.pk))
		super(DefaultEnvManagerAppVirtualBox, self).kill(job)

	

