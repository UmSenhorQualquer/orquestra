import traceback, inspect
from django.apps import apps
from pyforms_web.basewidget import BaseWidget
from confapp import conf

# Used for older python version
try:
    ModuleNotFoundError
except:
    class ModuleNotFoundError(Exception):
        pass


class AppsManager(object):

    def __init__(self):
        self._plugins_list = []
        self.search_4_plugins()

    def append(self, plugin): self._plugins_list.append(plugin)

    @property
    def plugins(self): return self._plugins_list

    
    def menu(self, user=None, menus=None):
        res = []

        for plugin_class in self.plugins:
            if not hasattr(plugin_class, 'ORQUESTRA_MENU'): continue
            if  menus and \
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

            plugin_class.fullname = '{0}.{1}'.format( plugin_class.__module__,plugin_class.__name__)

        return res



    def export_settings(self, filename):
        out = open(filename, 'w')

        apps = {}
        
        for plugin_class in self.plugins:
            if issubclass(plugin_class, BaseWidget):
                print(plugin_class)
                apps[plugin_class.__name__.lower()] = '{0}.{1}'.format(
                    plugin_class.__module__,
                    plugin_class.__name__
                )

        out.write( "PYFORMS_APPS = "+str(apps) )
        out.close()


    def search_4_plugins(self):
        for app in apps.get_app_configs():
            try:
                apss_modulename = '{0}.apps'.format(app.module.__name__)

                apps_module = __import__( apss_modulename, fromlist=[''] )
                
                for name in dir(apps_module):
                    obj = getattr(apps_module, name)
                    if inspect.isclass(obj) and hasattr(obj, 'LAYOUT_POSITION'):
                        self.append( obj )
                """
                except ModuleNotFoundError:
                    if conf.ORQUESTRA_SHOW_NO_MODULE_EXCEPTION:
                        traceback.print_exc()
                    pass
                """
            except ModuleNotFoundError:
                if conf.ORQUESTRA_SHOW_NO_MODULE_EXCEPTION:
                    traceback.print_exc()
            except:
                traceback.print_exc()
                
