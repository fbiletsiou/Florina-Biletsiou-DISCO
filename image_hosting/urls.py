from django.urls import include, path, re_path
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'images', viewset=views.UploadedFileViewset, basename='UploadedFile')
router.register(r'users', viewset=views.UserViewset, basename='User')


# Wiring up the API using automatic URL routing.
# Additionally, including login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^exp/generate/(?P<file_id>[0-9]+)/$', views.TempUrlViewset.as_view({'get': 'generate_link'})),
    re_path(r'^exp/use/(?P<token>[-a-zA-Z0-9_]+)/$', views.TempUrlViewset.as_view({'get': 'use'})),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

