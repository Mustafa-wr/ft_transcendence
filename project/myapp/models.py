from django.db import models
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your models here.
class user_data(models.Model):
    name = models.CharField(max_length=20, blank= False)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=20)
    status = models.CharField(max_length=5, default='')
    otp = models.CharField(max_length=6, default='')

    def __str__(self):
        return self.name
    
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