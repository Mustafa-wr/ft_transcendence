from django.urls import include, path
from . import views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('profile/', views.edit, name='edit'),
    path('profile/edit', views.edit, name='edit'),
    path('profile/stats', views.stats, name='stats'),
    path('profile/friends', views.friends, name='friends'),
    path('logout/', views.logout, name='logout'),
]