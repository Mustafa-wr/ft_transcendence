from django.apps import AppConfig
from django.db import models
from django import forms

# Create your models here.
class user_profile(models.Model):
	login = models.CharField(max_length=100, default='default_value')
	nickname = models.CharField(max_length=100, default='default_value')
	email = models.EmailField(max_length=100, default='default_value')
	image_link = models.CharField(max_length=150, default='default_value')
	preferred_language = models.CharField(max_length=12, default='English')
	two_factor_auth_status = models.CharField(max_length=12, default='Disabled')
	status = models.CharField(max_length=20, default='offline')
	image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
	@property
	def wins(self):
		return self.won_matches.count()

	@property
	def losses(self):
		return self.lost_matches.count()

	def __str__(self):
		return self.login

class match_record(models.Model):
	match_date = models.DateField()
	match_time = models.TimeField()
	match_winner = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='won_matches')
	match_loser = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='lost_matches')
	winner_score = models.IntegerField()
	loser_score = models.IntegerField()

class user_friends(models.Model):
	user = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='friends')
	friend = models.ForeignKey(user_profile, on_delete=models.CASCADE, related_name='friends_of')

	class Meta:
		unique_together = (('user', 'friend'),)

class PongSpaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
