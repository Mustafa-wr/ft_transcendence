from django import forms
from . import models

class Create_match_record(forms.ModelForm):
    class Meta:
        model = models.match_record
        fields = ['match_winner', 'match_loser', 'winner_score', 'loser_score']