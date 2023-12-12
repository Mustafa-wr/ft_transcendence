from django.db import models

# Create your models here.
class user_data(models.Model):
    name = models.CharField(max_length=20, blank= False)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=20)
    status = models.CharField(max_length=5, default='')
    otp = models.CharField(max_length=6, default='')

    def __str__(self):
        return self.name