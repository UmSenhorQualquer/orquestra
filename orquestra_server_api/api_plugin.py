
from orquestra.plugins.baseplugin import BasePlugin, LayoutPositions, StringArgType, IntArgType
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response
import os, csv
import simplejson, os, inspect
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import simplejson, json, glob, inspect, mimetypes, os
from pyforms import conf

from maestro.models import AlgorithmSubject, Algorithm, Server, Job

from pyforms_web.web.django_pyforms import ApplicationsLoader
from django.http import StreamingHttpResponse


class OrquestraApi(BasePlugin):

	menu = None

	@staticmethod
	def get_application(request, application):
		algo = Algorithm.objects.get(algorithm_name=application)
		a = {
			'algorithm_id':			algo.algorithm_id, 
			'algorithm_name':		algo.algorithm_name,
			'algorithm_class':		algo.algorithm_class,
			'algorithm_desc':		algo.algorithm_desc,
			'algorithmsubjects':	';'.join([str(x) for x in algo.algorithmsubjects.all()]),
		}
		data = simplejson.dumps( a )
		return HttpResponse(data, "application/json")
	get_application_argstype = [StringArgType]

	@staticmethod
	def app_parameters(request, application):
		model 			  = ApplicationsLoader.createInstance(application)
		model.httpRequest = request		
		data = simplejson.dumps( model.serializeForm() )
		return HttpResponse(data, "application/json")
	app_parameters_argstype = [StringArgType]


	@staticmethod
	def list_files(request):
		storage 	= conf.MAESTRO_STORAGE_MANAGER.get(request.user)
		path 		= request.POST.get('path', '/')

		print(request.POST)

		files 		= []
		for index, f in enumerate(storage.list(path)):
			files.append({
				'filename': 		f.filename,
				'fullpath': 		f.fullpath,
				'type': 			f.type, 
				'size': 		 	f.size,
				'last modified': 	f.lastmodified,				
			})

		data = simplejson.dumps( files )
		return HttpResponse(data, "application/json")
	list_files_argstype = []

	@staticmethod
	def upload_file(request):
		path 	 = request.POST.get('path','/')
		filename = request.FILES.get('file', None).name
		
		storage = conf.MAESTRO_STORAGE_MANAGER.get(request.user)

		filepath = os.path.join(path, filename)
		storage.put_file_contents(filepath, request.FILES['file'])
		fileinfo = storage.file_info( filepath )
		
		file_dict = {
			'name' : 			fileinfo.filename,
			'size' : 			fileinfo.size,			
		}

		data = simplejson.dumps( file_dict )
		return HttpResponse(data, "application/json")
	upload_file_argstype = []

	@staticmethod
	def download_file(request):
		path 	 = request.POST.get('path',None)
		
		storage = conf.MAESTRO_STORAGE_MANAGER.get(request.user)
		handler = storage.get_file_handler(path)
		
		response = StreamingHttpResponse(handler)
		filename = os.path.basename(path)
		response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
	
		return response
	download_file_argstype = []

	@staticmethod
	def delete_file(request):
		path 	 	= request.POST.get('path',None)
		storage 	= conf.MAESTRO_STORAGE_MANAGER.get(request.user)
		storage.delete(path)
		return HttpResponse(json.dumps({'RESPONSE':'OK'}), "application/json")
	delete_file_argstype = []

	@staticmethod
	def create_folder(request):
		path 	 	= request.POST.get('path',None)
		storage 	= conf.MAESTRO_STORAGE_MANAGER.get(request.user)
		storage.mkdir(path)
		return HttpResponse(json.dumps({'RESPONSE':'OK'}), "application/json")
	create_folder_argstype = []
