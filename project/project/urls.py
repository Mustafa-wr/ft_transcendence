from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)