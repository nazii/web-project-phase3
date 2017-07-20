from django.contrib import admin

# Register your models here.
from blog.models import Weblog, Post, Comment

admin.site.register(Weblog)
admin.site.register(Post)
admin.site.register(Comment)
