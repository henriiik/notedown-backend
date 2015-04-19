from api.models import Note
from django.contrib.auth.models import User
from rest_framework import serializers, fields


class UserSerializer(serializers.ModelSerializer):
    url = fields.CharField(source='googleauth.url')

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'url')


class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Note
        fields = ('id', 'content', 'created', 'edited', 'user', 'public')
