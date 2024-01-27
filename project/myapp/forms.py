from django import forms
from .models import user_profile

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = user_profile
		fields = ['nickname', 'image']
