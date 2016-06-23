import os, paramiko
from StringIO import StringIO
from fabric.api import *
from opencsp.envmanagers.EnvManager import EnvManager
from fabric.contrib.files import exists
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo
from django.utils import timezone
from django.conf import settings
from opencsp.envmanagers.DefaultEnvManager.fabproject import rsync_project
import subprocess
import socket
from opencsp import AVAILABLE_STORAGES


import socket
import struct

def wake_on_lan(macaddress, ipaddress, port=9):
	""" Switches on remote computers using WOL. """

	# Check macaddress format and try to compensate.
	if len(macaddress) == 12: pass
	elif len(macaddress) == 12 + 5: sep = macaddress[2]; macaddress = macaddress.replace(sep, '')
	else: raise ValueError('Incorrect MAC address format')

	# Pad the synchronization stream.
	data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
	send_data = '' 

	# Split up the hex values and pack.
	for i in range(0, len(data), 2): send_data = ''.join([send_data, struct.pack('B', int(data[i: i + 2], 16))])

	# Broadcast it to the LAN.
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.settimeout(1.0)
	sock.sendto(send_data, (ipaddress, port))
	

class SFTPFileBuffer:
	def __init__(self, filehandler):
		self._filehandler = filehandler

	def __iter__(self): return self

	def next(self):
		data = self._filehandler.read(32768)
		if len(data) <= 0:  raise StopIteration	
		return data

class DefaultEnvManager(EnvManager):


	def initCredentials(self, server):
		env.host_string 		= server.host_string
		env.password 			= server.password
		env.disable_known_hosts = True
		

	#######################################################################################
	##### Unitary operations ##############################################################
	#######################################################################################

	def exists(self, server, path):
		self.initCredentials(server)
		return exists(path)

	def put(self, server, origin, destiny): 
		self.initCredentials(server)
		#run(	"mkdir 	-p %s    " % destiny 	)
		#run(	"chmod 	-R 777 %s" % destiny    )
		put( origin, destiny)

	def get(self, server, origin, destiny): 
		self.initCredentials(server)
		get( origin, destiny)

	def write(self, server, filename, content):
		self.initCredentials(server)
		if isinstance(content, (int,float,long,str)):  content = StringIO(content)
		#print type(content)
		#print type(content), hasattr(content, 'read')
		put(content, filename)
		#run("echo -e '%s' > %s" % (content, filename) )	

		#self.transport = paramiko.Transport( (server.server_host, 22) )
		#self.transport.connect(username=username, password=password)
		#self.sftp = paramiko.SFTPClient.from_transport(self.transport)

	def read(self, server, filename):
		self.initCredentials(server)
		if exists(os.path.join( server.running_env,filename) ): 
			buf = StringIO(); get(os.path.join( server.running_env,filename), buf)
			return buf.getvalue()
		return ''

	def remove_files_in(self, server, folder):
		self.initCredentials(server)
		run("rm -rf %s" % os.path.join(server.remotedir, folder, '*') )

	def run(self, server, command):
		self.initCredentials(server)
		return run(command)
	
	def sudo(self, server, command):
		self.initCredentials(server)
		sudo(command)

	#######################################################################################
	##### Node setup related ##############################################################
	#######################################################################################

	def setup_node(self, server):
		"""
		Setup common features to several nodes in the same remote server
		"""
		self.initCredentials(server)
		#Creates the remote server directory	
		server.run("mkdir 	-p {0}".format(server.remotedir) 	)
		
		server.run("chmod 	-R 777 {0}".format(server.remotedir)    )
		server.run("echo 	{0} > {1}".format( server.pk, os.path.join( server.remotedir, "server_id.txt") )  )

		command = 'wget -O- {0}/ws/checknewjobs/{1}/'.format(settings.OPENCSP_URL, server.pk)
		server.run('echo 	"{0}" > {1}'.format( command, os.path.join( server.remotedir, "stop.sh") )  )

		#Sync the slave environment
		local_dir  = os.path.join(settings.BASE_DIR,'slave','*')
		remote_dir = server.remotedir

		print (server.server_pass.strip())>0, server.server_pass
		rsync_project(
			local_dir = local_dir,
			remote_dir= remote_dir,
			exclude=('.svn','*.pyc','applications','running_env'),
			delete=True,
			sshpass=(len(server.server_pass.strip())>0)
		)


	
	def setup_application(self, server, application):
		"""
		Setup the node environment in the remote server
		"""
		self.initCredentials(server)
		#Synchronize the application attributed to this server
		local_dir  = os.path.join(settings.PYFORMS_APPLICATIONS_PATH,application.algorithm_class.lower() )
		remote_dir = os.path.join(server.remotedir,'applications' )

		server.run("mkdir 	-p {0}".format(remote_dir) 	)
		server.run("chmod 	-R 777 {0}".format(remote_dir)    )
		
		rsync_project(
			local_dir = local_dir,
			remote_dir= remote_dir,
			exclude=('.svn','*.pyc','output'),
			delete=True,
			sshpass=(len(server.server_pass.strip())>0)
		)

		server.run( """echo "\nPYFORMS_MODE = 'TERMINAL'\n" >> {0}""".format( os.path.join(remote_dir, application.algorithm_class.lower(),'settings.py') ))
		


	#######################################################################################
	##### Server info #####################################################################
	#######################################################################################

	def server_info(self, server):
		if server.satelliteserver!=None: return "Isn't possible to retreave the status of a remote server"

		self.initCredentials(server)
		out = ''
		#out += str(run("df -h"))
		#out += "\n\n----------------------------------------------------------------------------------------------------------------" 
		out += "\n\n" + str(run("top -n 1 -b | head"))
		return out

	def server_checkconnection(self, server):
		"""
		Verify if the remote server is alive
		"""
		try:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1.0)
				port = 2222 if hasattr(server, 'virtualserver') else 22
				s.connect((server.server_host, port)); v = s.recv(1024); s.close()
				return len(v)>10
			except socket.error as e: 
				return False
			finally:
				s.close()
		except: pass
		return False

	def turnon_server(self, server):
		"Turn the computer on"
		if 	server.server_host!=None and server.server_mac!=None and \
			server.server_host!='' 	 and server.server_mac!='':
			
			wake_on_lan(server.server_mac, server.server_host, port=9)
			wake_on_lan(server.server_mac, '<broadcast>', port=9)
		
	def turnoff_server(self, server):
		"Turn the computer off"
		if server.server_host and server.server_mac and server.server_turnoff:
			self.sudo(server,  'shutdown -h now')

	#######################################################################################
	##### Jobs related ####################################################################
	#######################################################################################

	def has_job(self, server):
		#if server.reservedto!=None: return True

		from opencsp.models import Job, Server
		#If has a started job, then return True
		if Job.objects.exclude(job_started=None).filter(server=server, job_ended=None).exists(): return True

		if server.parent==None:
			#If the server is parent server, then check his childs
			childs = Server.objects.filter(parent=server)
			for child in childs: 
				if child.has_job(): return True
		else:
			#If the server is a child, check his parent
			return Job.objects.exclude(job_started=None).filter(server=server.parent, job_ended=None).exists()
	
		return False

	def is_busy(self, server): return server.exists( os.path.join(server.running_env,'busy.yes') )

	def read_output(self, job):
		server = job.server
		self.initCredentials(server)
		if exists(os.path.join( server.running_env,'output.txt') ): 
			buf = StringIO(); get(os.path.join( server.running_env,'output.txt'), buf)
			return buf.getvalue()
		return ''

	def output_files(self, job, directories=False):
		server = job.server
		self.initCredentials(server)
		path = os.path.join(server.running_env, 'output') 
		try:
			if directories:
				string = run("find %s/* -type d" % path)
			else:
				string = run("find %s/* -type f" % path)
		except:
			return []
		files = string.replace("\r","").split("\n")
		pathsize = len(path)
		files = [ x[pathsize+1:] for x in files ]
		return files

	def server_jobinfo(self, job):
		server = job.server
		self.initCredentials(server)
		out = ''
		
		try:
			out += str(run("top -n 1 -b | head -n 15"))			
		except:
			out += 'Error on calling top'
		
		try:
			out += "\n\n----------------------------------------------------------------------------"
			out += "\n\n" + str( run("ls -R -lh {0}".format( os.path.join(server.running_env, 'output') ) ) )
		except:
			out += '\n\nError happend, on checking the output folder'

		return out

	def set_busy(self, job): 
		server = job.server
		self.initCredentials(server)

		server.run( "mkdir -p %s" 	% server.running_env )
		server.run( "chmod 777 %s" % server.running_env )

		run( "echo %d > %s" % (job.pk, os.path.join( server.running_env,'busy.yes')  ) )

	def remote_script(self, job):
		params = ' '.join( job.consoleparameters )
		appPath = os.path.join( job.server.remotedir,"applications", job.job_application.lower(), job.job_application+'.py' )
		frameworkPath = os.path.join( job.server.remotedir,"framework" )
		stopPath = os.path.join( job.server.remotedir,"stop.sh" )
		command = "PYTHONPATH={2} python {0} {1} --exec execute >output.txt 2>&1\n".format(appPath, params, frameworkPath)
		command += "mv busy.yes busy.no >>output.txt 2>&1\n"
		command += "sh {0} >>output.txt 2>&1\n".format(stopPath)

		return command
		

	def create_remote_script(self, job):
		shellscript = os.path.join( job.server.running_env, 'run.sh')
		job.server.write( shellscript , self.remote_script(job) )
		job.server.run( "chmod u+x {0}".format(shellscript) )


	def prepare_job(self, job):
		server = job.server

		server.write( os.path.join(server.running_env, 'server_id.txt') , server.server_id )
		server.run( "mkdir %s" 	% os.path.join(server.running_env, 'output') )
		server.run( "chmod 777 %s" % os.path.join(server.running_env, 'output') )

		server.run( "mkdir %s" 	% os.path.join(server.running_env, 'input') )
		server.run( "chmod 777 %s" % os.path.join(server.running_env, 'input') )
		
		destiny_folder = os.path.join( server.running_env, 'input' )
		
		job.job_uploadedBytes = 0
		storage = AVAILABLE_STORAGES.get(job.user)

		job.info("Loading slave server:")
		for filepath in job.inputfiles:
			print "\t{0} -> server".format(filepath)
			job.info( "\t{0} -> server".format(filepath) )
			filehandler = storage.get_file_handler(filepath)

			filename = os.path.join(destiny_folder, filepath[1:] )
			server.run( "mkdir -p '%s'" % os.path.dirname(filename) )
			job.server.write(filename, filehandler )
			
			fileinfo = storage.file_info( filepath )
			job.job_uploadedBytes += fileinfo.size

		job.save()

		
		self.create_remote_script(job)
		print "Files loaded"
	

	def run_job(self, job): 
		print "run job " + ('cd %s; sh run.sh' % job.server.running_env)
		job.server.paramikoRun( 'cd %s; sh run.sh' % job.server.running_env )


	def remote_path_size(self, server, path):
		try:
			out = server.run("du -sbc {0}".format( os.path.join(path,'*') ) )
		except:
			return 0
		return int(out.split()[-2])

	def local_path_size(self, path):
		return int(subprocess.check_output(['du','-sb', path]).split()[0].decode('utf-8'))

	def unload_files(self, job, userpath):
		server = job.server
		outputFolder = os.path.join( server.running_env, 'output')

		job.job_startDownload = timezone.now()
		job.job_downloadedBytes = 0
		job.job_outparameters = self.read(server, 'out-parameters.txt')

		#try:
		job.info("Downloading job's output:")
		if server.exists( outputFolder ):
			job.job_outputSize = self.remote_path_size(server, outputFolder)
			job.info("du -sb {0}".format(outputFolder))
			job.save()

			storage = AVAILABLE_STORAGES.get(job.user)

			client = paramiko.SSHClient()
			client.load_system_host_keys()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			
			if server.password!=None and len(server.password)>0:
				client.connect( server.server_host, timeout=5.0, username=server.server_user, password=server.password)
			elif server.server_certificate!=None and len(server.server_certificate)>0:
				client.connect( server.server_host, timeout=20.0, username=server.server_user, key_filename=server.server_certificate)
			else:
				client.connect( server.server_host, timeout=5.0, username=server.server_user, look_for_keys=True)
			
			sftp_client = client.open_sftp()

			params = eval(str(job.job_parameters)); userpath = params['userpath']
			
			for f in server.output_files(job, directories=True):
				if len(f.strip())==0: continue
				job.info( "\t{0} <- {1}".format(userpath, f) )	
				directory_path = os.path.join( userpath, f )
				storage.mkdir( directory_path )
				
			for f in server.output_files(job, directories=False):
				if len(f.strip())==0: continue
				job.info( "\t{0} <- {1}".format(userpath, f) )	
				filepath = os.path.join( userpath, f )

				filehandler = sftp_client.file( os.path.join( outputFolder, f ) , 'rb')
				filehandler.prefetch()
				filebuffer = SFTPFileBuffer(filehandler)
				try:
					storage.put_file_contents( filepath, filebuffer )
				finally: 
					filehandler.close() 

				fileinfo = storage.file_info( filepath )
				job.job_downloadedBytes += fileinfo.size
		#except Exception, e: 
		#	job.error( str(e) )

		job.job_endDownload = timezone.now()
		job.save()

		


	def kill(self, job):
		job.info("Killing job {0}".format(job.pk))
		
		if job.server.exists(os.path.join(job.server.running_env, 'pid.txt') ):
			job.server.run(
				'cd {0}; sh {1} >> output.txt'.format(job.server.running_env, os.path.join(job.server.remotedir, 'kill.sh') )
			)