from django.shortcuts 								import render_to_response
from django.contrib.auth.decorators 				import login_required
from orquestra.management.commands.install_plugins 	import PluginsManager
from orquestra.plugins.baseplugin 					import MenusPositions

@login_required
def index(request):
	manager = PluginsManager()
	context = {'user': request.user}

	context.update({
		'plugins': 		[plugin() for plugin in manager.plugins],
		'menu_plugins': manager.menu(request.user, menus=[MenusPositions.MAIN_MENU, MenusPositions.USER_MENU]) 
	})
	return render_to_response('authenticated_base.html', context )