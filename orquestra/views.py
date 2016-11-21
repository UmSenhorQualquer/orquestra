from django.shortcuts 								import render_to_response
from django.contrib.auth.decorators 				import login_required
from orquestra.management.commands.install_plugins 	import PluginsManager
from orquestra.plugins.baseplugin 					import MenusPositions

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
	for plugin_class in manager.menu(request.user, menus=[MenusPositions.MAIN_MENU, MenusPositions.USER_MENU]):
		print plugin_class.menu
		menus += [(
				plugin_class.menu, 
				plugin_class.label, 
				plugin_class.icon if hasattr(plugin_class, 'icon') else None, 
				plugin_class.__name__.lower(), 
				"run{0}();".format( plugin_class.__name__.capitalize())
				)]

	context.update({
		'menu_plugins': menus,
		'styles_files': style_files,
		'javascript_files': javascript_files,
	})
	return render_to_response('authenticated_base.html', context )