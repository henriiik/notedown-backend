import datetime
import json
import urllib.parse
import urllib.request

from api.models import GoogleAuth, Note
from api.serializers import UserSerializer, NoteSerializer
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from urllib.error import HTTPError


def urlopen(url, data=None):
    request = urllib.request.Request(url, data)
    response = urllib.request.urlopen(request)
    response = response.read()
    response = response.decode('utf-8')
    response = json.loads(response)
    return response


def post(url, data):
    data = urllib.parse.urlencode(data).encode('utf-8')
    return urlopen(url, data)


def get(url, data):
    data = urllib.parse.urlencode(data)
    url = '{}?{}'.format(url, data)
    return urlopen(url)


class LoginView(APIView):

    def post(self, request, format=None):
        try:
            token_url = 'https://accounts.google.com/o/oauth2/token'
            token_data = {
                'code': request.data['code'],
                'client_id': settings.GOOGLE_CLIENT_ID,
                'client_secret': settings.GOOGLE_CLIENT_SECRET,
                'redirect_uri': 'postmessage',
                'grant_type': 'authorization_code',
                }
            token_response = post(token_url, token_data)
            info_url = 'https://accounts.google.com/o/oauth2/tokeninfo'
            info_data = {
                'access_token': token_response['access_token'],
                }
            info_response = post(info_url, info_data)
            profile_url = 'https://www.googleapis.com/plus/v1/people/me'
            profile_response = get(profile_url, info_data)
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
            auth_info = GoogleAuth(
                google_user_id=info_response['user_id'],
                user=user
                )

        from pprint import pprint
        pprint(profile_response)

        auth_info.user.email = info_response['email']
        auth_info.user.first_name = profile_response['name']['givenName']
        auth_info.user.last_name = profile_response['name']['familyName']
        auth_info.user.save()

        auth_info.access_token = token_response['access_token']
        auth_info.id_token = token_response['id_token']
        auth_info.verified_email = info_response['verified_email']
        auth_info.url = profile_response.get('url', '')
        auth_info.expiration = (timezone.now() + datetime.timedelta(
            seconds=token_response['expires_in']))
        auth_info.save()

        token, created = Token.objects.get_or_create(user=auth_info.user)

        return Response({
            'token': token.key,
            'userId': auth_info.user_id
        })


class ErrorView(APIView):

    def some_function(self):
        raise Exception('OH NO!')

    def get(self, request, format=None):
        self.some_function()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class NoteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return self.queryset.filter(
                    Q(public=True) | Q(user=self.request.user)
                )
        return self.queryset.filter(public=True)
