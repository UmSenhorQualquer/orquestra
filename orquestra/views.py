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

	plugins4menus = sorted(manager.menu(request.user), key=lambda x: x.menu )
	menus 		  = []
	active_menus  = []

	parent_menu   = None
	for plugin_class in plugins4menus:
		menus_options = plugin_class.menu.split('>')
		
		active_menus.append( menus_options[0] )
		
		menu 			= type('MenuOption', (object,), {})
		menu.menu_place	= menus_options[0]
		menu.uid 		= plugin_class._uid if hasattr(plugin_class,'_uid') else ''
		menu.label 		= plugin_class.label
		menu.order 		= plugin_class.menu_order if hasattr(plugin_class,'menu_order') else None
		menu.icon  		= plugin_class.icon if hasattr(plugin_class, 'icon') else None
		menu.anchor 	= plugin_class.__name__.lower()
		menu.js_call 	= "run{0}();".format( plugin_class.__name__.capitalize())
		menu.submenus 	= []

		if len(menus_options)==1:
			menus.append(menu)

		elif parent_menu is None and len(menus_options)==2:
			parent_menu 				= type('ParentMenuOption', (object,), {})
			parent_menu.menu_place		= menus_options[0]
			parent_menu.label 			= menus_options[1]
			parent_menu.order 			= plugin_class.menu_order if hasattr(plugin_class,'menu_order') else None
			parent_menu.icon 			= plugin_class.parent_icon if hasattr(plugin_class,'parent_icon') else None
			parent_menu.submenus 		= []
			parent_menu.submenus.append(menu)
			menus.append(parent_menu)

		elif parent_menu.menu_place==menu.menu_place and menus_options[1]==parent_menu.label:
			parent_menu.submenus.append(menu)
			if not parent_menu.icon:
				parent_menu.icon = plugin_class.parent_icon if hasattr(plugin_class,'parent_icon') else None

		elif parent_menu.menu_place==menu.menu_place or menus_options[1]!=parent_menu.label:
			parent_menu 				= type('ParentMenuOption', (object,), {})
			parent_menu.menu_place		= menus_options[0]
			parent_menu.label 			= menus_options[1]
			parent_menu.order 			= plugin_class.menu_order if hasattr(plugin_class,'menu_order') else None
			parent_menu.icon 			= plugin_class.parent_icon if hasattr(plugin_class,'parent_icon') else None
			parent_menu.submenus 		= []
			parent_menu.submenus.append(menu)
			menus.append(parent_menu)

		else:
			menus.append(menu)

	
	menus = sorted(menus, key=lambda x: x.order)
	for menu in menus:
		menu.submenus = sorted(menu.submenus, key=lambda x: x.order)

	context.update({
		'menu_plugins': menus,
		'active_menus': list(set(active_menus)),
		'styles_files': style_files,
		'javascript_files': javascript_files,
	})
	return render_to_response('authenticated_base.html', context )

