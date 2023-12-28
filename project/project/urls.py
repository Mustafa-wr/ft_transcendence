"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myapp.views import index
from myapp.views import home
from myapp.views import game
from myapp.views import base
from myapp.views import authorize
from myapp.aouth import callback
from django.conf.urls.i18n import i18n_patterns
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
    path('game/', game),
    path('base/', base),
    path('authorize/', authorize, name='authorize'),
    path('callback/', callback, name='callback'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('debug/', include('debug_toolbar.urls')),
]

urlpatterns += i18n_patterns (
   path('', include('myapp.urls')),
)


