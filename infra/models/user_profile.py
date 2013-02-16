from django.db import models
from django.contrib.auth.models import User
from django.conf.global_settings import LANGUAGES

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True,null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)
    lang=models.CharField(max_length=12,null=True,blank=True,default='en',
                          choices=LANGUAGES)
    overview=models.TextField(null=True,blank=True)

    class Meta:
        app_label = 'infra'

