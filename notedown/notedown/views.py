from django.contrib.auth.models import User
from rest_framework import viewsets
from notedown.serializers import UserSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
