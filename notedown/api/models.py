from django.db import models
from django.contrib.auth.models import User


class GoogleAuth(models.Model):
    user = models.OneToOneField(User)
    google_user_id = models.CharField(max_length=100)
    expiration = models.DateTimeField()
    access_token = models.CharField(max_length=100)
    id_token = models.TextField()
    verified_email = models.BooleanField()


class Note(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]
