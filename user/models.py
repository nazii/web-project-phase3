from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Token(models.Model):
    token = models.CharField()
    user = models.ForeignKey(User)
