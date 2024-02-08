from django.urls import include, path
from . import views
from django.urls import include, path

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('game/', views.game, name='game'),
    path('pong/', views.pong, name='pong'),
    path('profile/', views.edit, name='edit'),
    path('profile/edit', views.edit, name='edit'),
    path('profile/stats', views.stats, name='stats'),
    path('profile/friends', views.friends, name='friends'),
    path('logout/', views.logout, name='logout'),
]




