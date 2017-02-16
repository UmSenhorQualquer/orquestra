import os, simplejson
from django.http 									import HttpResponse
from django.shortcuts 								import render_to_response
from django.contrib.auth.decorators 				import login_required
from orquestra.management.commands.install_plugins 	import PluginsManager
from orquestra.plugins 			 					import MenusPositions
from pyforms_web.web.djangoapp 						import ApplicationsLoader

@login_required
def index(request):
	manager = PluginsManager()
	context = {'user': request.user}

	style_files, javascript_files = [], []
	for plugin in manager.plugins:
		for staticfile in (plugin.static_files if hasattr(plugin, 'static_files') else []):
			if staticfile.endswith('.css'): style_files.append(staticfile)
			if staticfile.endswith('.js'):  javascript_files.append(staticfile)

	plugins4menus = sorted(manager.menu(request.user), key=lambda x: x.label )
	menus 		  = []

	parent_menu   = None
	for plugin_class in plugins4menus:
		labels = plugin_class.label.split('>')

		menu 			= type('MenuOption', (object,), {})
		menu.menu_name	= labels[0]
		menu.label 		= labels[-1]
		menu.icon  		= plugin_class.icon if hasattr(plugin_class, 'icon') else None
		menu.anchor 	= plugin_class.__name__.lower()
		menu.js_call 	= "run{0}();".format( plugin_class.__name__.capitalize())
		menu.submenus 	= []


		if parent_menu is None and len(labels)==3:
			parent_menu 				= type('ParentMenuOption', (object,), {})
			parent_menu.menu_name		= labels[0]
			parent_menu.label 			= labels[1]
			parent_menu.submenus 		= []
			parent_menu.submenus.append(menu)
			menus.append(parent_menu)

		elif len(labels)==2:
			menus.append(menu)

		elif parent_menu.menu_name==menu.menu_name and len(labels)==3 and labels[1]==parent_menu.label:
			parent_menu.submenus.append(menu)

		elif parent_menu.menu_name==menu.menu_name or labels[1]!=parent_menu.label:
			parent_menu 				= type('ParentMenuOption', (object,), {})
			parent_menu.menu_name		= labels[0]
			parent_menu.label 			= labels[1]
			parent_menu.submenus 		= []
			parent_menu.submenus.append(menu)
			menus.append(parent_menu)

	
	context.update({
		'menu_plugins': menus,
		'styles_files': style_files,
		'javascript_files': javascript_files,
	})
	return render_to_response('authenticated_base.html', context )

