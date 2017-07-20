# Register your models here.
from django.contrib import admin

from user.models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'user_token')
admin.site.register(Token, TokenAdmin)
