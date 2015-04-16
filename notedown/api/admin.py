from django.contrib import admin
from api.models import GoogleAuth, Note


class GoogleAuthAdmin(admin.ModelAdmin):
    list_display = ('user', 'expiration')

admin.site.register(GoogleAuth, GoogleAuthAdmin)


class NoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'edited')

admin.site.register(Note, NoteAdmin)
