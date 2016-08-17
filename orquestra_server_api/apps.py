from django.apps import AppConfig

class OrquestraServerApiPluginConfig(AppConfig):
	name = 'orquestra_server_api'
	verbose_name = "Orquestra API"

	orquestra_plugins = [
		'orquestra_server_api.api_plugin.OrquestraApi',
	]