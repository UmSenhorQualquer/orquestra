from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

class Command(BaseCommand):
    help = 'Setup orquestra plugins'

    def handle(self, *args, **options):
       	for app in apps.get_app_configs():
       		if hasattr(app, 'orquestra_plugin'):
       			print "install plugin"