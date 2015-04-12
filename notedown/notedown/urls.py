from django.conf.urls import include, url
from django.contrib import admin
from api.views import UserViewSet, LoginView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^login/?$', LoginView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
]
