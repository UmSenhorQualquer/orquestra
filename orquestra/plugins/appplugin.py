import inspect, os
from orquestra.plugins.baseplugin import BasePlugin
from pyforms_web.web.django import ApplicationsLoader
from django.shortcuts import render_to_response
from django.template import RequestContext

class AppPlugin(BasePlugin):

	@staticmethod
	def render_app(request, app_module, template=None):
		model 				= ApplicationsLoader.createInstance(app_module)
		model.httpRequest 	= request
		model_path 			= inspect.getfile(model.__class__)

		if template==None: template = os.path.join('pyforms', 'pyforms-template.html')

		params = { 'application': app_module, 'appInstance': model}
		params.update( model.initForm() )

		return render_to_response(template,params, context_instance=RequestContext(request))
		