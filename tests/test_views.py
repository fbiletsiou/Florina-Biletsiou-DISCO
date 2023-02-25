import datetime

import pytest

from django.urls import reverse

from tests.fixtures import *
from image_hosting.models import randomString


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


class TestExpiryLink:

    def test_generating_link_view_unauthorized(self, client):
        url = reverse('generate_link', kwargs={'file_id': 1})
        response = client.get(url)
        assert response.status_code == 401

    def test_generating_link_view_basic_authorized(self, api_client, get_or_create_token, create_file, get_or_create_basic_user):
        basic_user = get_or_create_basic_user

        token = get_or_create_token(basic_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        file = create_file('png', basic_user)
        url = reverse('generate_link', kwargs={'file_id': file.pk})
        response = api_client.get(url)

        assert response.status_code == 403
        assert response.data.get('error') == 'Given account tier does not support this feature'

    def test_generating_link_view_premium_authorized(self, api_client, get_or_create_token, create_file, get_or_create_premium_user):
        premium_user = get_or_create_premium_user

        token = get_or_create_token(premium_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        file = create_file('png', premium_user)
        url = reverse('generate_link', kwargs={'file_id': file.pk})
        response = api_client.get(url)

        assert response.status_code == 403
        assert response.data.get('error') == 'Given account tier does not support this feature'

    def test_generating_link_view_enterprise_wrong_time_authorized(self, api_client, get_or_create_token, create_file, get_or_create_enterprise_user):
        enterprise_user = get_or_create_enterprise_user

        token = get_or_create_token(enterprise_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        file = create_file('png', enterprise_user)
        url = reverse('generate_link', kwargs={'file_id': file.pk}) + '?time=999999'
        response = api_client.get(url)

        assert response.status_code == 400
        assert response.data.get('error') == 'Time requested: 999999. Allowed range: 300-30000'

    def test_generating_link_view_enterprise_authorized(self, api_client, get_or_create_token, create_file, get_or_create_enterprise_user):
        enterprise_user = get_or_create_enterprise_user

        token = get_or_create_token(enterprise_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        file = create_file('png', enterprise_user)
        url = reverse('generate_link', kwargs={'file_id': file.pk}) + '?time=4000'
        response = api_client.get(url)

        assert response.status_code == 201
        assert list(response.data.keys()) == ['id', 'expiry_date', 'temp_url']

    def test_using_link_view_unauthorized(self, client):
        url = reverse('use_link', kwargs={'token': 'qqqqqqqqq'})
        response = client.get(url)
        assert response.status_code == 401

    def test_using_link_view_basic_authorized(self, api_client, get_or_create_token, create_file, get_or_create_basic_user):
        basic_user = get_or_create_basic_user

        token = get_or_create_token(basic_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('use_link', kwargs={'token': 'qqqqqqqqq'})
        response = api_client.get(url)

        assert response.status_code == 403
        assert response.data.get('error') == 'Given account tier does not support this feature'

    def test_using_link_view_premium_authorized(self, api_client, get_or_create_token, create_file, get_or_create_premium_user):
        premium_user = get_or_create_premium_user

        token = get_or_create_token(premium_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        url = reverse('use_link', kwargs={'token': 'qqqqqqqqq'})
        response = api_client.get(url)

        assert response.status_code == 403
        assert response.data.get('error') == 'Given account tier does not support this feature'

    def test_using_link_view_enterprise_authorized(self, api_client, get_or_create_token, create_file, create_temp_url, get_or_create_enterprise_user):
        enterprise_user = get_or_create_enterprise_user

        token = get_or_create_token(enterprise_user)
        api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        file = create_file('png', enterprise_user)
        temp_url = create_temp_url(user=enterprise_user, token=randomString(stringLength=20),file=file, expiry_date=datetime.datetime.now() + datetime.timedelta(seconds=400))

        url = reverse('use_link', kwargs={'token': temp_url.token})
        response = api_client.get(url)

        assert response.status_code == 302
        assert response.url == f"/images/{file.id}/"

