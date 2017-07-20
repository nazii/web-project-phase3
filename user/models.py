from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Token(models.Model):
    token = models.CharField(max_length=100)
    user = models.ForeignKey(User)

    def user_token(self):
        return self.user.username


