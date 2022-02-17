import inspect
import traceback

from confapp import conf
from django.apps import apps

from pyforms_web.basewidget import BaseWidget


class AppsManager(object):

    def __init__(self):
        self._plugins_list = []
        self.search_4_plugins()

    def append(self, plugin):
        self._plugins_list.append(plugin)

    @property
    def plugins(self):
        return self._plugins_list

    def menu(self, user=None, menus=None):
        res = []

        for plugin_class in self.plugins:
            if not hasattr(plugin_class, 'ORQUESTRA_MENU'): continue
            if menus and \
                    (
                            not hasattr(plugin_class, 'ORQUESTRA_MENU') or \
                            not plugin_class.ORQUESTRA_MENU in menus
                    ): continue

            add = False

            if hasattr(plugin_class, 'has_permissions'):
                if plugin_class.has_permissions(user):
                    add = True
            else:
                add = True

            if add: res.append(plugin_class)

            plugin_class.fullname = '{0}.{1}'.format(plugin_class.__module__, plugin_class.__name__)

        return res

    def export_settings(self, filename):
        out = open(filename, 'w')

        apps = {}

        for plugin_class in self.plugins:
            if issubclass(plugin_class, BaseWidget):
                apps[plugin_class.__name__.lower()] = '{0}.{1}'.format(
                    plugin_class.__module__,
                    plugin_class.__name__
                )

        out.write("PYFORMS_APPS = " + str(apps))
        out.close()

    def search_4_plugins(self):
        places = ['pyforms_apps', 'pyforms_apps']

        for place in places:
            for app in apps.get_app_configs():
                try:
                    apss_modulename = f'{app.module.__name__}.{place}'
                    apps_module = __import__(apss_modulename, fromlist=[''])
                    for name in dir(apps_module):
                        obj = getattr(apps_module, name)
                        if inspect.isclass(obj) and hasattr(obj, 'LAYOUT_POSITION'):
                            self.append(obj)

                except ModuleNotFoundError:
                    pass
                except ImportError:
                    if conf.PYFORMS_VERBOSE:
                        traceback.print_exc()
                except:
                    traceback.print_exc()
