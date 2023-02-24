import os
import tempfile
import uuid
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from image_hosting.models import UploadedFile
from image_hosting.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_password():
    return 'strong-test-pass'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        # return django_user_model.objects.create_user(**kwargs)
        return User.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_jpg_file(db):
    from io import BytesIO
    from PIL import Image
    from django.core.files.uploadedfile import InMemoryUploadedFile

    image = Image.new('RGB', (100, 100))
    with tempfile.NamedTemporaryFile(suffix='.png') as image_file :
        image.save(image_file)

        return UploadedFile.objects.create(name=image_file.name, file_format=UploadedFile.ValidFileFormat.PNG, file_size=100, image_url=image_file.name)


@pytest.fixture
def get_or_create_token(db, create_user):
    user = create_user()
    token, _ = Token.objects.get_or_create(user=user)
    return token
