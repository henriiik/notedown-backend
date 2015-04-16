from api.models import Note
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class NoteSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Note
        fields = ('id', 'content', 'edited', 'user')
