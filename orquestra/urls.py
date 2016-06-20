"""orquestra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls  import url, include, patterns
from django.contrib    import admin
from django.conf import settings
from proscenium.views  import *

urlpatterns = [
    url(r'^$', index),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^pyforms/', include('pyforms_web.web.django.urls') ),
    url(r'^admin/', admin.site.urls),
]


if settings.DEBUG:
	urlpatterns = patterns(
		'',
		url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
		url(r'', include('django.contrib.staticfiles.urls')),
	) + urlpatterns