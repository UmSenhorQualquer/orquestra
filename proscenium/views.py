from django.shortcuts 						import render_to_response
from django.contrib.auth.decorators 		import login_required

@login_required
def index(request):
	context = {'user': request.user}
	#context.update({ 'plugins':OPENCSP_PLUGINS.menu(request.user, menus=[MenusPositions.MAIN_MENU, MenusPositions.USER_MENU]) })
	return render_to_response('authenticated_base.html', context )