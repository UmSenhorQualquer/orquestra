import inspect, os
from orquestra.plugins.baseplugin import BasePlugin
from pyforms_web.web.django import ApplicationsLoader
from django.shortcuts import render_to_response
from django.template import RequestContext
from pyforms_web.web.django.views import Apps2Update

class AppPlugin(BasePlugin):

	@staticmethod
	def render_app(request, app_module, template=None):
		app  = ApplicationsLoader.create_instance(request, app_module)
		params = { 'application': app_module, 'appInstance': app}
		params.update( app.init_form() )

		if template==None: template = os.path.join('pyforms', 'pyforms-template.html')
		return render_to_response(template,params)
		