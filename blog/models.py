from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Weblog(models.Model):
    user = models.ForeignKey(User)
    weblog_name = models.CharField(max_length=20)
    is_default = models.BooleanField()
    post_words = models.TextField(default="")

    def weblog_user(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=20)
    writer_name = models.CharField(max_length=20)
    datetime = models.FloatField()
    summary = models.TextField()
    text = models.TextField()
    weblog = models.ForeignKey(Weblog)


class Comment(models.Model):
    text = models.TextField()
    datetime = models.FloatField()
    post = models.ForeignKey(Post)
