from django.contrib import admin
from .models import user_profile, match_record, user_friends

# Register your models here.
admin.site.register(user_profile)
admin.site.register(match_record)
admin.site.register(user_friends)
