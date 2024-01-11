from django.contrib import admin
from django.urls import path, include
from myapp import views
from myapp.views import authorize
from myapp.aouth import callback
from django.conf.urls.i18n import i18n_patterns
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('', include('myapp.urls')),
    path('authorize/', authorize, name='authorize'),
    path('callback/', callback, name='callback'),
    path('debug/', include('debug_toolbar.urls')),
]

urlpatterns += i18n_patterns (
   path('', include('myapp.urls')),
   prefix_default_language=False,
)


