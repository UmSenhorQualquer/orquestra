from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

import inspect, os, shutil, pkgutil, importlib
from django.conf import settings
from django.conf.urls import url
from django.template.loader import render_to_string
from orquestra.orquestra_plugin import LayoutPositions, OrquestraPlugin


class PluginsManager(object):

	def __init__(self):
		self._plugins_list = []
		self.search_4_plugins()

	def append(self, plugin):
		self._plugins_list.append(plugin)

	def urls(self):
		params = ['']

		for plugin in self._plugins_list:
			if hasattr(plugin,'top_view_url'):
				params.append( 
					url( plugin.top_view_url, plugin.top_view, name="%s-top" % plugin._hash ) 
				)
			if hasattr(plugin,'bottom_view_url'):
				params.append( 
					url( plugin.bottom_view_url, plugin.bottom_view, name="%s-bottom" % plugin._hash )
				)
		
		return params

	@property
	def plugins(self): return self._plugins_list

	
	def menu(self, user=None, menus=None):
		res = []
		for plugin in self._plugins_list:
			if menus!=None and not plugin.menu in menus: continue
			
			add = False
			if hasattr(plugin, 'groups'):
				if 'superuser' in plugin.groups and user.is_superuser:  add = True
				if user.groups.filter(name__in=plugin.groups).exists():  add = True
			else:
				add = True

			if add: res.append(plugin)

		return res


	def copy_static_files(self, static_folder):

		static_folder = os.path.join(static_folder, 'plugins')
		if not os.path.exists(static_folder): os.makedirs(static_folder)

		for p in self.plugins:
			class_file = inspect.getfile(p)
			print os.path.realpath(class_file), '-'
			plugin_folder = os.path.dirname(os.path.realpath(class_file))
			print plugin_folder
			for filename in p.static_files:
				shutil.copyfile( os.path.join(plugin_folder, filename),os.path.join(static_folder, filename))


	def export_urls_file(self, filename):
		out = open(filename, 'w')

		out.write( "from django.conf.urls import url\n" )
		for plugin in self.plugins:
			out.write( 
				"from {0} import {1}\n".format(
					plugin.__module__,
					plugin.__name__
				) 
			)
		out.write( "\n" )

		out.write( "urlpatterns = [\n" )
		for pluginClass in self.plugins:
			plugin = pluginClass()
			
			for view in plugin.views:
				if not hasattr(plugin, '%s_argstype' % view.__name__): continue
				if hasattr(plugin, '%s_name' % view.__name__):
					out.write( "\turl(r'^{0}', {1}, name='{2}'),\n".format( 
						OrquestraPlugin.viewURL(pluginClass, view), 
						OrquestraPlugin.viewName(pluginClass, view),
						getattr(plugin, '%s_name' % view.__name__)
					))
				else:
					out.write( "\turl(r'^%s', %s),\n" % ( 
						OrquestraPlugin.viewURL(pluginClass, view), 
						OrquestraPlugin.viewName(pluginClass, view) ) )
		out.write( "]" )

		out.close()



	def export_js_file(self, filename):
		out = open(filename, 'w')
		
		for pluginClass in self.plugins:
			plugin = pluginClass()
			for view in plugin.views:
				if not hasattr(plugin, '%s_position' % view.__name__): continue
				if not hasattr(plugin, '%s_argstype' % view.__name__): continue

				prefix = pluginClass.__name__.capitalize()
				sufix = view.__name__.capitalize()
				if prefix==sufix: sufix=''
				params = [x for x in inspect.getargspec(view)[0][1:]]
				out.write( "function run%s%s(%s){\n" % ( prefix, sufix, ','.join(params) ) )
				out.write( "\tloading();\n" )
				out.write( "\tactivateMenu('menu-%s');\n" % plugin.anchor )

				position = getattr(plugin, '%s_position' % view.__name__)
				
				label_attr = '{0}_label'.format(view.__name__)
				label = getattr(plugin, label_attr) if hasattr(plugin, label_attr) else view.__name__
				
				breadcrumbs = OrquestraPlugin.viewBreadcrumbs(plugin, view)
				#if position==LayoutPositions.TOP:
				#	out.write( "\tshowBreadcrumbs(%s, '%s');\n" % (breadcrumbs, label) )
				
				
				if hasattr(plugin, '%s_js' % view.__name__):
					javascript = getattr(plugin, '%s_js' % view.__name__)
					out.write( """\t%s\n""" % javascript )
				else:		
					if position==LayoutPositions.HOME:
						out.write( "\tclearInterval(refreshEvent);\n")
						out.write( """
						select_main_tab();
						$('#top-pane').load("/plugins/%s", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});\n""" % OrquestraPlugin.viewJsURL(pluginClass, view) )
					
					if position==LayoutPositions.NEW_TAB:

						out.write('add_tab("{0}", "{1}", "/plugins/{2}");'.format(view.__name__, label, OrquestraPlugin.viewJsURL(pluginClass, view)) )

					if position==LayoutPositions.WINDOW:
						out.write( "\tloading();" )
						out.write( "\t$('#opencsp-window').dialog('open');\n" )
						out.write( """\t$('#opencsp-window').load("/plugins/%s",function() {\n"""  %  OrquestraPlugin.viewJsURL(pluginClass, view) )
						out.write( """\t\tnot_loading();$(this).scrollTop($(this)[0].scrollHeight);\n""" )
						out.write( """\t});\n""" )
					if position==LayoutPositions.NEW_WINDOW:
						out.write( """window.open('/plugins/%s');""" % OrquestraPlugin.viewJsURL(pluginClass, view) )

				out.write( "}\n" )
				out.write( "\n" )
			
		views_ifs = []
		for pluginClass in self.plugins:
			plugin = pluginClass()
			for view in plugin.views:
				prefix = pluginClass.__name__.capitalize()
				sufix = view.__name__.capitalize()
				if prefix==sufix: sufix=''
				params = [x for x in inspect.getargspec(view)[0][1:]]
				views_ifs.append( "\tif(view=='%s') run%s%s.apply(null, params);\n" % ( OrquestraPlugin.viewJsAnchor(pluginClass, view), prefix, sufix) )


		out.write( render_to_string( os.path.join( os.path.dirname(__file__), '..', '..','templates','plugins','commands.js'), {'views_ifs': views_ifs} ) )
		out.close()


	def search_4_plugins(self):
		
		for app in apps.get_app_configs():
			if not(hasattr(app, 'orquestra_plugin') and app.orquestra_plugin): continue
			
			pkg_dir = app.module.__path__
			for module_loader, name, ispkg in pkgutil.iter_modules(pkg_dir):
				module = importlib.import_module('.{0}'.format(name), app.module.__name__)
				for key in dir(module):
					attr = getattr(module, key)
					if inspect.isclass(attr) \
					   and isinstance(attr, type) and \
					   str(attr.__module__)==str(module.__name__) and \
					   issubclass(attr, OrquestraPlugin):
						
						self.append(attr)









OUTPUT_PLUGINS_DIR = os.path.join( settings.BASE_DIR, 'orquestra_plugins')


class Command(BaseCommand):
	help = 'Setup orquestra plugins'

	def handle(self, *args, **options):
		manager = PluginsManager()


		if not os.path.exists(OUTPUT_PLUGINS_DIR): os.makedirs(OUTPUT_PLUGINS_DIR)
		manager.export_urls_file( os.path.join(OUTPUT_PLUGINS_DIR,'urls.py') )
		
		static_dir = os.path.join(OUTPUT_PLUGINS_DIR, 'static')
		if not os.path.exists(static_dir): os.makedirs(static_dir)

		js_dir = os.path.join(static_dir, 'js')
		if not os.path.exists(js_dir): os.makedirs(js_dir)
		

		print("Updating plugins scripts")
		manager.export_js_file( os.path.join(js_dir,'commands.js') )
		manager.copy_static_files(settings.STATIC_ROOT)

		#environment_file = os.path.join(OUTPUT_PLUGINS_DIR,'environments.py')
		#self.export_environments(environment_file)