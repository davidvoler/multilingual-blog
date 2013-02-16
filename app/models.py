# Define a custom User class to work with django-social-auth
from django.db import models
from django.contrib.auth.models import User
from infra.models.user_profile import UserProfile

class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        user=self.model._default_manager.create(username=username,
                                                  email=email)
        prof=UserProfile(user=user)
        prof.save()
        return user

class CustomUser(User):
    class Meta:
        proxy = True
    def is_authenticated(self):
        return True
