from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import traceback

import inspect, os, shutil, pkgutil, importlib
from django.conf import settings
from pysettings import conf
from django.conf.urls import url
from django.template.loader import render_to_string
from orquestra.plugins import LayoutPositions
from pyforms_web.web.BaseWidget import BaseWidget


class PluginsManager(object):

	def __init__(self):
		self._plugins_list = []
		self.search_4_plugins()

	def append(self, plugin): self._plugins_list.append(plugin)

	@property
	def plugins(self): return self._plugins_list

	
	def menu(self, user=None, menus=None):
		res = []

		for plugin_class in self.plugins:
			if not hasattr(plugin_class, 'ORQUESTRA_MENU'): continue
			if 	menus and \
				(
					not hasattr(plugin_class, 'ORQUESTRA_MENU') or \
					not plugin_class.ORQUESTRA_MENU in menus
				): continue

			add = False
			if hasattr(plugin_class, 'AUTHORIZED_GROUPS'):
				if 'superuser' in plugin_class.AUTHORIZED_GROUPS and user.is_superuser:   add = True
				if user.groups.filter(name__in=plugin_class.AUTHORIZED_GROUPS).exists():  add = True
			else:
				add = True

			if add: res.append(plugin_class)

			plugin_class.fullname = '{0}.{1}'.format( plugin_class.__module__,plugin_class.__name__)

		return res



	def export_settings(self, filename):
		out = open(filename, 'w')

		apps = {}
		
		for plugin_class in self.plugins:
			if issubclass(plugin_class, BaseWidget):
				print(plugin_class)
				apps[plugin_class.__name__.lower()] = '{0}.{1}'.format(
					plugin_class.__module__,
					plugin_class.__name__
				)

		out.write( "PYFORMS_APPS = "+str(apps) )
		out.close()


	def search_4_plugins(self):
		for app in apps.get_app_configs():
			try:
				apss_modulename = '{0}.apps'.format(app.module.__name__)

				apps_module = __import__( apss_modulename, fromlist=[''] )
				
				for name in dir(apps_module):
					obj = getattr(apps_module, name)
					if inspect.isclass(obj) and hasattr(obj, 'LAYOUT_POSITION'):
						self.append( obj )

			except:
				#print(app)
				traceback.print_exc()

class Command(BaseCommand):
	help = 'Setup orquestra plugins'

	def handle(self, *args, **options):
		manager = PluginsManager()

		static_dir = os.path.join( settings.BASE_DIR, 'pyforms_plugins')
		if not os.path.exists(static_dir): os.makedirs(static_dir)

		f = open(os.path.join(static_dir,'__init__.py'), 'w')
		f.write("from pysettings import conf\nconf += 'pyforms_plugins.settings'")
		f.close()
		
		manager.export_settings(os.path.join(static_dir,'settings.py'))