from django.contrib import admin

# Register your models here.
from blog.models import Weblog, Post, Comment


class WeblogAdmin(admin.ModelAdmin):
    list_display = ('id', 'weblog_name', 'is_default', 'weblog_user')
    list_filter = ('weblog_name', 'is_default')

admin.site.register(Weblog, WeblogAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    list_filter = ('title', 'datetime', 'writer_name')

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id',)
admin.site.register(Comment, CommentAdmin)
