import pytest

from django.urls import reverse

from tests.fixtures import *


@pytest.mark.django_db
def test_view(client):
    url = reverse('api-root')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
class TestUploadedFileViewsets:

    def test_list_view_unauthorized(self, client):
        url = reverse('UploadedFile-list')
        response = client.get(url)
        assert response.status_code == 401

    def test_list_view_authorized(self, api_client, get_or_create_token):
        url = reverse('UploadedFile-list')
        token = get_or_create_token
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_detail_view_unauthorized(self, client):
        url = reverse('UploadedFile-detail')
        response = client.get(url)
        assert response.status_code == 401

    def test_detail_view_authorized(self, api_client, get_or_create_token, create_jpg_file):
        file = create_jpg_file
        url = reverse('UploadedFile-list', kwargs={'pk': file.pk})
        token = get_or_create_token
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestUserViewsets:

    def test_list_view_unauthorized(self, client):
        url = reverse('User-list')
        response = client.get(url)
        assert response.status_code == 401

    def test_list_view_authorized(self, admin_client):
        url = reverse('User-list')

        response = admin_client.get(url)
        assert response.status_code == 200

"""
'^images/(?P<pk>[^/.]+)/$' [name='UploadedFile-detail']>
'^images/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='UploadedFile-detail']
'^users/$' [name='User-list']
'^users\.(?P<format>[a-z0-9]+)/?$' [name='User-list']
'^users/(?P<pk>[^/.]+)/$' [name='User-detail']
'^users/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$' [name='User-detail']
"""
