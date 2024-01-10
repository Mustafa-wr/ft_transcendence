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

# Nart's Models
class User(models.Model):
	nickname = models.CharField(max_length=50, default="None")
	intra_username = models.CharField(max_length=50, unique=True, default="None")
	email = models.EmailField(max_length=100, default='None')
	image_link = models.CharField(max_length=150, default='None')
	current_status = models.CharField(max_length=10, default="Offline")
	# preferred_language = models.CharField(max_length=20, default="English")    ->>>>> mustafa has commented this line
	wins = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)

	def __str__(self):
		return self.login

class Match(models.Model):
	match_date = models.DateField()
	match_time = models.TimeField()
	winner_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='won_matches')
	loser_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lost_matches')
	winner_score = models.IntegerField()
	loser_score = models.IntegerField()

class UserFriends(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
	friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_of')

	class Meta:
		unique_together = (('user', 'friend'),)

class UserMatches(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	match = models.ForeignKey(Match, on_delete=models.CASCADE)

	class Meta:
		unique_together = (('user', 'match'),)
