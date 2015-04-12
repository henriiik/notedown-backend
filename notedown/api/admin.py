from django.contrib import admin
from api.models import GoogleAuth


class GoogleAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'expiration')

admin.site.register(GoogleAuth, GoogleAuthAdmin)
