from django.db import models

# Create your models here.

class Weblog(models.Model) :
    user = models.ForeignKey(User)
    weblog_name = models.CharField()
    is_default = models.BooleanField()

class Post(models.Model) :
    title = models.CharField()
    writer_name = models.CharField()
    datetime = models.DateField()
    summary = models.TextField()
    text = models.TextField()
    weblog = models.ForeignKey(Weblog)

class Comment(models.Model) :
    text = models.TextField()
    datetime = models.DateField()
    post = models.ForeignKey(Post)