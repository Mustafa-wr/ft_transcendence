from django.apps import AppConfig
from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.
class user_data(models.Model):
    login = models.CharField(max_length=100, default='default_value')
    nickname = models.CharField(max_length=100, default='default_value')
    email = models.EmailField(max_length=100, default='default_value')
    image_link = models.CharField(max_length=150, default='default_value')
    status = models.CharField(max_length=20, default='offline')
    win = models.IntegerField(default=0)
    loses = models.IntegerField(default=0)

    def __str__(self):
        return self.login

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = (
			'username',
			'email',
			'password1',
			'password2',
		)



class PongSpaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
