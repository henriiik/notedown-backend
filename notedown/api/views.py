import datetime
import json
import urllib.parse
import urllib.request

from api.models import GoogleAuth
from api.serializers import UserSerializer
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.error import HTTPError


class LoginView(APIView):

    def post(self, request, format=None):
        try:
            token_url = 'https://accounts.google.com/o/oauth2/token'
            token_data = urllib.parse.urlencode({
                'code': request.data['code'],
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': 'postmessage',
                'grant_type': 'authorization_code'
                }).encode('utf-8')
            token_request = urllib.request.Request(token_url, token_data)
            token_response = urllib.request.urlopen(token_request)
            token_response = token_response.read()
            token_response = token_response.decode('utf-8')
            token_response = json.loads(token_response)
            info_url = 'https://accounts.google.com/o/oauth2/tokeninfo'
            info_data = urllib.parse.urlencode({
                'access_token': token_response['access_token'],
                }).encode('utf-8')
            info_request = urllib.request.Request(info_url, info_data)
            info_response = urllib.request.urlopen(info_request)
            info_response = info_response.read()
            info_response = info_response.decode('utf-8')
            info_response = json.loads(info_response)
        except HTTPError as e:
            error = e.read()
            error = error.decode('utf-8')
            error = json.loads(error)
            return Response(data=error, status=e.code)

        try:
            auth_info = GoogleAuth.objects.get(
                google_user_id=info_response['user_id'])
        except GoogleAuth.DoesNotExist:
            user, created = User.objects.get_or_create(
                username=info_response['user_id'])
            user.email = info_response['email']
            user.save()
            auth_info = GoogleAuth(
                google_user_id=info_response['user_id'],
                user=user
                )

        auth_info.access_token = token_response['access_token']
        auth_info.id_token = token_response['id_token']
        auth_info.verified_email = info_response['verified_email']
        auth_info.expiration = (timezone.now() + datetime.timedelta(
            seconds=token_response['expires_in']))
        auth_info.save()

        token, created = Token.objects.get_or_create(user=auth_info.user)

        return Response({'token': token.key})


class ErrorView(APIView):

    def some_function(self):
        raise Exception('OH NO!')

    def get(self, request, format=None):
        self.some_function()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
