from confapp import conf
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render

from orquestra.apps_manager import AppsManager


def index(request, app_uid=None):
    manager = AppsManager()
    plugins = manager.plugins

    # no plugins are available.
    # it will show the default application
    if len(plugins) == 0:
        return render(request, 'orquestra/default-app.html')

    if conf.ORQUESTRA_REQUIREAUTH and \
            not request.user.is_authenticated:
        return HttpResponseRedirect(settings.LOGIN_URL)

    ##### find the style and javscripts files #################################################
    style_files, javascript_files = [], []
    for plugin in plugins:
        if hasattr(plugin, 'STATIC_FILES'):
            for staticfile in plugin.STATIC_FILES:
                if staticfile.endswith('.css'): style_files.append(staticfile)
                if staticfile.endswith('.js'):  javascript_files.append(staticfile)
    ###########################################################################################

    #### load menus ###########################################################################
    plugins4menus = list(set(manager.menu(request.user)))
    plugins4menus = sorted(plugins4menus, key=lambda x: (x.ORQUESTRA_MENU, len(x.ORQUESTRA_MENU)))
    menus = {}
    active_menus = {}

    running_menu = None

    for plugin_class in plugins4menus:
        menus_options = plugin_class.ORQUESTRA_MENU.split('>', maxsplit=1)

        menu_place = menus_options[0]

        # If no menu top was configured all apps will be shown on the left menu
        if menu_place == 'top' and not conf.ORQUESTRA_HAS_TOP_BAR:
            menu_place = 'left'

        menu_label = None
        if len(menus_options) == 2:
            menu_label = menus_options[1]
            if menu_label != plugin_class.__name__ and menus_options[1] not in menus:
                menu = type('MenuOption', (object,), {})
                menu.menu_place = menu_place
                menu.label = menu_label
                menu.submenus = []
                menu.icon = None
                menu.order = plugin_class.ORQUESTRA_MENU_ORDER if hasattr(plugin_class, 'ORQUESTRA_MENU_ORDER') else None
                menus[menu_label] = menu

        # used to check if a menu should be activated or not
        active_menus[menu_place] = True

        # if an application is not running ignore the submenus
        # if app_uid is None and len(menus_options) > 1:
        #    continue

        menu = type('MenuOption', (object,), {})
        menu.menu_place = menu_place
        menu.uid = plugin_class.UID if hasattr(plugin_class, 'UID') else ''
        menu.url = plugin_class.ORQUESTRA_URL if hasattr(plugin_class, 'ORQUESTRA_URL') else '/app/{0}/'.format(menu.uid)
        menu.target = 'target={0}'.format(plugin_class.ORQUESTRA_TARGET) if hasattr(plugin_class, 'ORQUESTRA_TARGET') else ''
        menu.label = plugin_class.TITLE if plugin_class.TITLE else plugin_class.__name__.lower()
        menu.order = plugin_class.ORQUESTRA_MENU_ORDER if hasattr(plugin_class, 'ORQUESTRA_MENU_ORDER') else None
        menu.icon = plugin_class.ORQUESTRA_MENU_ICON if hasattr(plugin_class, 'ORQUESTRA_MENU_ICON') else None
        menu.anchor = plugin_class.__name__.lower()
        menu.fullname = plugin_class.fullname  # full name of the class
        menu.js_call = getattr(plugin_class, 'js_call', None)
        menu.parent_menu = None
        menu.active = False
        menu.submenu_active = False
        menu.submenus = []
        menu.show_submenu = False

        # append main menu
        if len(menus_options) == 1:
            menus[plugin_class.__name__] = menu

        elif len(menus_options) == 2:
            parent_menu = menus.get(menu_label, None)
            if parent_menu is None:
                parent_menu = menus[menu_label] = menu

            if parent_menu:
                menu.parent_menu = parent_menu
                parent_menu.submenus.append(menu)
                # menu.parent_menu.active = True

        if hasattr(plugin_class, 'UID') and app_uid == plugin_class.UID:
            running_menu = menu
            menu.active = True
            if menu.parent_menu:
                menu.parent_menu.show_submenu = True
                menu.parent_menu.submenu_active = True
            else:
                menu.show_submenu = True

    ## sort menus and submenus ######################################################################
    menus = sorted(menus.values(), key=lambda x: (x.menu_place, x.order))
    final_menus = []
    for menu in menus:
        if not hasattr(menu, 'uid') and len(menu.submenus) == 0:
            continue
        menu.submenus = sorted(menu.submenus, key=lambda x: x.order)
        final_menus.append(menu)
    menus = final_menus
    #################################################################################################

    if running_menu is None and len(menus) > 0 and app_uid is None:
        running_menu = sorted(menus, key=lambda x: x.order)[0]

    context = {'user': request.user}
    context.update({
        'title': conf.ORQUESTRA_PAGE_TITLE,
        'submenu_title': conf.ORQUESTRA_TITLE,
        'menu_plugins': menus,
        'active_menus': list(set(active_menus)),
        'styles_files': style_files,
        'javascript_files': javascript_files,
        'running_menu': running_menu,
        'GOOGLE_ANALYTICS': conf.ORQUESTRA_GOOGLE_ANALYTICS,
        'extra_css_file': conf.ORQUESTRA_EXTRA_CSS_FILE,
        'ORQUESTRA_HAS_TOP_BAR': conf.ORQUESTRA_HAS_TOP_BAR,
    })

    return render(request, 'orquestra/base-authenticated.html', context)
