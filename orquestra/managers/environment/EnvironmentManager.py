import inspect, os
from opencsp.tools import fromImport
import logging
from opencsp.envmanagers.Environments import ENVIRONMENTS
from django.conf import settings

class EnvironmentManager:

	def __init__(self):
		self._storage = ENVIRONMENTS

	def __importClass(self, moduleclassname, application=None):
		logging.debug("EnvironmentManager::__importClass({0},{1})".format(moduleclassname, str(application)))

		modulename  = (str(moduleclassname)+"App"+str(application)) if application else moduleclassname

		logging.debug("__importClass {0} {1} {2}".format(moduleclassname, application, modulename))
		if modulename not in ENVIRONMENTS.keys():

			logging.debug("__importClass from opencsp.envmanagers.{0}.{1} import {2}".format(moduleclassname, modulename, modulename) )
			moduleclass = fromImport('opencsp.envmanagers.{0}.{1}'.format(moduleclassname, modulename), modulename)
			moduleobj   = moduleclass()
			ENVIRONMENTS[modulename] = moduleobj
		else:
			moduleobj = ENVIRONMENTS[modulename]

		logging.debug("EnvironmentManager::__importClass({0},{1})::return {2}".format(moduleclassname, str(application), str(moduleobj)))
		return moduleobj


	def get(self, moduleclassname, application=None):
		logging.debug("EnvironmentManager::get({0},{1})".format(moduleclassname, str(application)))

		if moduleclassname==None or moduleclassname=='': moduleclassname = 'DefaultEnvManager'

		if application!=None:
			modulename = str(moduleclassname)+"App"+str(application)
			modulefile = os.path.join(settings.BASE_DIR,'opencsp','envmanagers',str(moduleclassname),modulename+'.py') 
			logging.debug("check if file exists {0}".format(modulefile))
			if os.path.exists( modulefile ): return self.__importClass(moduleclassname, application)
				
		modulename = str(moduleclassname)
		modulefile = os.path.join(settings.BASE_DIR,'opencsp','envmanagers',str(moduleclassname),moduleclassname+'.py') 
		logging.debug("check if file exists {0}".format(modulefile))
		if os.path.exists( modulefile ): return self.__importClass(modulename)

		return self.__importClass('DefaultEnvManager')

	@property
	def choices(self):
		res = []
		for key, item in ENVIRONMENTS.items():
			res.append( (key, key) )
		return tuple(res)

	

