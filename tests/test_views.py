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
        token = get_or_create_token()
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_detail_view_unauthorized(self, client):
        url = reverse('UploadedFile-detail', kwargs={'pk': 1})
        response = client.get(url)
        assert response.status_code == 401

    def test_detail_view_basic_authorized(self, api_client, get_or_create_token, create_file, get_or_create_basic_user):
        basic_user = get_or_create_basic_user

        token = get_or_create_token(basic_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        file = create_file('png', basic_user)
        url = reverse('UploadedFile-detail', kwargs={'pk': file.pk})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data.get('image_thumbnail200') is not None
        assert response.data.get('image_thumbnail400') is None

    def test_detail_view_premium_authorized(self, api_client, get_or_create_token, create_file, get_or_create_premium_user):
        premium_user = get_or_create_premium_user

        token = get_or_create_token(premium_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        file = create_file('png', premium_user)
        url = reverse('UploadedFile-detail', kwargs={'pk': file.pk})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data.get('image_thumbnail200') is not None
        assert response.data.get('image_thumbnail400') is not None

    def test_detail_view_enterprise_authorized(self, api_client, get_or_create_token, create_file, get_or_create_enterprise_user):
        enterpise_user = get_or_create_enterprise_user

        token = get_or_create_token(enterpise_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        file = create_file('png', enterpise_user)
        url = reverse('UploadedFile-detail', kwargs={'pk': file.pk})
        response = api_client.get(url)
        assert response.status_code == 200
        assert response.data.get('image_thumbnail200') is not None
        assert response.data.get('image_thumbnail400') is not None


@pytest.mark.django_db
class TestUserViewsets:

    def test_list_view_unauthorized(self, client):
        url = reverse('User-list')
        response = client.get(url)
        assert response.status_code == 401

    def test_list_view_authorized(self, api_client, get_or_create_admin_token):
        token = get_or_create_admin_token
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('User-list')

        response = api_client.get(url)
        assert response.status_code == 200

    def test_detail_view_unauthorized(self, client):
        url = reverse('User-detail', kwargs={'pk': 1})
        response = client.get(url)
        assert response.status_code == 401

    def test_detail_view_authorized(self, api_client, get_or_create_admin_token):
        token = get_or_create_admin_token
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        user = User.objects.all().first()

        url = reverse('User-detail', kwargs={'pk': user.pk})

        response = api_client.get(url)
        assert response.status_code == 200
        assert list(response.data.keys()) == ['id', 'username', 'tier', 'images', 'expiry_links']
