from django.apps import AppConfig
from django.db import models
from django import forms

# Create your models here.
class user_profile(models.Model):
	login = models.CharField(max_length=100, default='default_value')
	nickname = models.CharField(max_length=100, default='default_value')
	email = models.EmailField(max_length=100, default='default_value')
	image_link = models.CharField(max_length=150, default='default_value')
	status = models.CharField(max_length=20, default='offline')
	preferred_language = models.CharField(max_length=20, default="English")
	wins = models.IntegerField(default=0)
	losses = models.IntegerField(default=0)

	def __str__(self):
		return self.login
	


class Match_maker(models.Model):
	match_name = models.CharField(max_length=100, default='default_value')
	players = models.ManyToManyField(user_profile, related_name='players')

class Game(models.Model):
	player_1 = models.CharField(max_length=100, default='default_value')
	player_2 = models.CharField(max_length=100, default='default_value')
	player_1_score = models.IntegerField(default=0)
	player_2_score = models.IntegerField(default=0)

	
class tournament(models.Model):
	tournament_name = models.CharField(max_length=100, default='default_value')
	players = models.ManyToManyField(user_profile, related_name='tournament_players')
	#matches = models.ManyToManyField(match_record)
	


class match_record(models.Model):
	match_date = models.DateField(auto_now_add=True)
	match_time = models.TimeField(auto_now_add=True)
	match_winner = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='won_matches') # default=None
	match_loser = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='lost_matches')
	winner_score = models.IntegerField(default=0)
	loser_score = models.IntegerField(default=0)

class user_friends(models.Model):
	user = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='friends')
	friend = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='friends_of')

	class Meta:
		unique_together = (('user', 'friend'),)

class PongSpaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
