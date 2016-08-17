import os
from django.conf import settings as django_settings
from orquestra import settings as orquestra_settings
from pyforms_web.web.storage.storagemanager import StorageManager

class Settings(dict):

	def __getitem__(self, key):
		if os.environ.get(key, None): 			return os.environ.get(key)
		if hasattr(django_settings, key): 		return getattr(django_settings, key)
		if hasattr(orquestra_settings, key): 	return getattr(orquestra_settings, key)

		self.__init_variables_if_needed(key)

		return getattr(self, key)

	def __init_variables_if_needed(self, key):

		if key=='MAESTRO_STORAGE_MANAGER' and not hasattr(self, 'MAESTRO_STORAGE_MANAGER'):
			self.MAESTRO_STORAGE_MANAGER 		= StorageManager( self['MAESTRO_STORAGES_INTERFACES'] )

		if key=='MAESTRO_ENVIRONMENT_MANAGER' and not hasattr(self, 'MAESTRO_ENVIRONMENT_MANAGER'):
			self.MAESTRO_ENVIRONMENT_MANAGER 	= EnvironmentManager( self['MAESTRO_ENVIRONMENT_INTERFACES'] )
		
settings = Settings()