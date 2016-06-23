import os


class EnvManager(object):

	def __init__(self): pass

	#######################################################################################
	##### Unitary operations ##############################################################
	#######################################################################################

	def exists(self, server, path): 
		"""
		Check if a file exists in the remote server
		"""
		pass

	def put(self, server, origin, destiny, data=None): 
		"""
		Upload a file to the remote server
		"""
		pass

	def get(self, server, origin, destiny):
		"""
		Download a file from the remote server
		"""
		pass

	def run(self, server, command):
		"""
		Run a command in the remote server
		"""
		return None

	def sudo(self, server, command):
		"""
		Run a command in the remote server as sudo
		"""
		return None

	def write(self, server, filename, content):
		"""
		Write a file in the remote server
		"""
		pass

	def remove_files_in(self, server, folder): 
		"""
		Remove all files in the path of the remote server
		"""
		pass


	#######################################################################################
	##### Node setup related ##############################################################
	#######################################################################################

	def setup_node(self, server):
		"""
		Setup the node environment in the remote server
		"""
		pass
	
	def setup_application(self, server, application):
		"""
		Setup the application associated to the node
		"""
		pass

	def close_setup_node(self, server, application):
		"""
		Setup the application associated to the node
		"""
		pass

	#######################################################################################
	##### Server info #####################################################################
	#######################################################################################

	def server_info(self, server): 
		"""
		Return information about the remote server
		"""
		return ''

	def server_checkconnection(self, server):
		"Return if the server is on or off"
		return False

	def turnon_server(self, server):
		"Turn the computer on"
		pass

	#######################################################################################
	##### Jobs related ####################################################################
	#######################################################################################
	
	def has_job(self, server): 
		"""
		Check if the server has a job registered in the database
		"""
		return False

	def is_busy(self, server): 
		"""
		Check in the remote host if the server is busy with a job
		"""
		return False

	def set_busy(self, job): 
		"""
		Create a flag in the remote host signing that it is reserved for a job execution
		"""
		pass

	def read_output(self, job): 
		"""
		get the remote server output during the execution of a job
		"""
		return ""

	def output_files(self, job):
		"""
		Return a list of files in the output directory of the remote server
		"""
		return []
	
	def server_jobinfo(self, job):
		"""
		Return information about the remote server when a job is running
		"""
		return ""

	def remote_script(self, job):
		"""
		Construct the remote script content
		"""
		return ""

	def create_remote_script(self, job):
		"""
		Create a script file in the remote server used to run the job
		"""
		pass
	
	def prepare_job(self, job):
		"""
		Prepare the job for execution in the remote server
		"""
		pass

	def run_job(self, job):
		"""
		Start the job in the remote server
		"""

	def unload_files(self, job, userpath):
		"""
		Unload the files from the remote output directory from a previous Job
		"""

	def kill(self, job):
		"""
		Kill job in the remote server
		"""