from django.apps import AppConfig
from django.db import models
from django import forms
from django.contrib.auth.models import User

class user_profile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.first())
	login = models.CharField(max_length=100, default='default_value')
	nickname = models.CharField(max_length=100, default='default_value')
	email = models.EmailField(max_length=100, default='default_value')
	image_link = models.CharField(max_length=150, default='default_value')
	preferred_language = models.CharField(max_length=12, default='English')
	# two_factor_auth_status = models.CharField(max_length=12, default='Disabled')
	status = models.CharField(max_length=20, default='offline')
	image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
	last_login = models.DateTimeField(default='2021-01-01 00:00:00')
	is_2fa_enabled = models.BooleanField(default=False)
	@property
	def wins(self):
		return self.won_matches.count()

	@property
	def losses(self):
		return self.lost_matches.count()

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

class Create_match_record(forms.ModelForm):
    class Meta:
        model = match_record
        fields = ['match_winner', 'match_loser', 'winner_score', 'loser_score']
