from confapp                        import conf
from django.conf                    import settings
from django.http                    import HttpResponseRedirect
from django.shortcuts               import render_to_response
from orquestra.apps_manager         import AppsManager


def index(request, app_uid=None):
    manager = AppsManager()
    plugins = manager.plugins

    # no plugins are available.
    # it will show the default application
    if len(plugins)==0:
        return render_to_response('default-app.html' )

    if  conf.ORQUESTRA_REQUIREAUTH and \
        not request.user.is_authenticated:
        return HttpResponseRedirect(settings.LOGIN_URL)
        
    
    ##### find the style and javscripts files #################################################
    style_files, javascript_files = [], []
    for plugin in plugins:
        for staticfile in plugin.STATIC_FILES:
            if staticfile.endswith('.css'): style_files.append(staticfile)
            if staticfile.endswith('.js'):  javascript_files.append(staticfile)
    ###########################################################################################

    #### load menus ###########################################################################
    plugins4menus = sorted(manager.menu(request.user), key=lambda x: (x.ORQUESTRA_MENU,len(x.ORQUESTRA_MENU)) )
    menus         = {}
    active_menus  = {}

    running_menu = None

    for plugin_class in plugins4menus:
        menus_options = plugin_class.ORQUESTRA_MENU.split('>')

        # used to check if a menu should be activated or not
        active_menus[menus_options[0]] = True

        # if an application is not running ignore the submenus
        if app_uid is None and len(menus_options)>1: continue
        
        menu            = type('MenuOption', (object,), {})
        menu.menu_place = menus_options[0]
        menu.uid        = plugin_class.UID if hasattr(plugin_class,'UID') else ''
        menu.url        = plugin_class.ORQUESTRA_URL if hasattr(plugin_class,'ORQUESTRA_URL') else '/app/{0}/'.format(menu.uid)
        menu.target     = 'target={0}'.format(plugin_class.ORQUESTRA_TARGET) if hasattr(plugin_class, 'ORQUESTRA_TARGET') else ''
        menu.label      = plugin_class.TITLE if plugin_class.TITLE else plugin_class.__name__.lower()
        menu.order      = plugin_class.ORQUESTRA_MENU_ORDER if hasattr(plugin_class,'ORQUESTRA_MENU_ORDER') else None
        menu.icon       = plugin_class.ORQUESTRA_MENU_ICON if hasattr(plugin_class, 'ORQUESTRA_MENU_ICON') else None
        menu.anchor     = plugin_class.__name__.lower()
        menu.fullname   = plugin_class.fullname # full name of the class
        menu.parent_menu= None
        menu.active     = False
        menu.submenu_active = False
        menu.submenus   = []
        menu.show_submenu = False
        
        # append main menu
        if len(menus_options)==1:
            menus[plugin_class.__name__] = menu
        
        elif len(menus_options)==2:
            parent_menu = menus.get(menus_options[1], None)
            if parent_menu:
                menu.parent_menu = parent_menu
                parent_menu.submenus.append( menu )
                #menu.parent_menu.active = True

        if hasattr(plugin_class, 'UID') and app_uid==plugin_class.UID: 
            running_menu = menu         
            menu.active  = True
            if menu.parent_menu: 
                menu.parent_menu.show_submenu = True
                menu.parent_menu.submenu_active = True
            else:
                menu.show_submenu = True

    ## sort menus and submenus ######################################################################
    menus = sorted(menus.values(), key=lambda x: (x.menu_place, x.order) )
    for menu in menus: menu.submenus = sorted(menu.submenus, key=lambda x: x.order)
    #################################################################################################

    if running_menu is None and len(menus)>0: running_menu = sorted(menus, key=lambda x: x.order )[0]

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
        'extra_css_file': conf.ORQUESTRA_EXTRA_CSS_FILE
    })

    return render_to_response('base-authenticated.html', context )

