from django.db import models
from django.contrib.auth.models import User


class GoogleAuth(models.Model):
    user = models.OneToOneField(User)
    google_user_id = models.CharField(max_length=100)
    expiration = models.DateTimeField()
    access_token = models.CharField(max_length=100)
    id_token = models.CharField(max_length=100)
    verified_email = models.BooleanField()
