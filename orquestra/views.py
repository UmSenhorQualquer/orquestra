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

	menus = []

	for plugin_class in manager.menu(request.user):
		menu = type('MenuOption', (object,), {})
		menu.topmenu 	= plugin_class.menu == MenusPositions.MAIN_MENU
		menu.usermenu 	= plugin_class.menu == MenusPositions.USER_MENU
		menu.order 		= plugin_class.menu_order
		menu.label 		= plugin_class.label
		menu.icon  		= plugin_class.icon if hasattr(plugin_class, 'icon') else None
		menu.anchor 	= plugin_class.__name__.lower()
		menu.js_call 	= "run{0}();".format( plugin_class.__name__.capitalize())
		menus.append(menu)


	menus = sorted(menus, key=lambda x: x.order)
	context.update({
		'menu_plugins': menus,
		'styles_files': style_files,
		'javascript_files': javascript_files,
	})
	return render_to_response('authenticated_base.html', context )

