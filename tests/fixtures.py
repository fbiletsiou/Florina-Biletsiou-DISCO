import tempfile
import uuid
import pytest
from PIL import Image
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

from image_hosting.models import User, UploadedFile, TempUrl


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
        if 'tier' in kwargs:
            if kwargs['tier'] == 'Basic':
                kwargs['tier'] = User.UserTiers.BASIC
            elif kwargs['tier'] == 'Premium':
                kwargs['tier'] = User.UserTiers.PREMIUM
            elif kwargs['tier'] == 'Enterprise':
                kwargs['tier'] = User.UserTiers.ENTERPRISE

        # return django_user_model.objects.create_user(**kwargs)
        return User.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_admin_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())

        kwargs['is_staff'] = True
        # return django_user_model.objects.create_user(**kwargs)
        return User.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_file(db, tmp_path_factory):
    def _create(extension, created_by):
        image = Image.new('RGB', (100, 100))
        temp_dir = 'C:\\Users\\FB\\Documents\\Florina-Biletsiou-DISCO-test\\media\\test_media'
        with tempfile.NamedTemporaryFile(suffix=f'.{extension}', dir=temp_dir, delete=False) as image_file:
            image.save(image_file)

            if extension =='png':
                file_format = UploadedFile.ValidFileFormat.PNG
            elif extension == 'jpg':
                file_format = UploadedFile.ValidFileFormat.JPEG
            else:
                return None

            new_file = UploadedFile.objects.create(name="test_file",
                                                   file_format=file_format,
                                                   image_url=image_file.name,
                                                   created_by=created_by)
            return new_file

    return _create


@pytest.fixture
def create_temp_url(db):
    def _create(user, token, file, expiry_date):

            new_url = TempUrl.objects.create(user=user,
                                             related_file=file,
                                             token=token,
                                             expiry_date=expiry_date)
            return new_url
    return _create


@pytest.fixture
def get_or_create_basic_user(db, create_user):
    basic_user = create_user(tier='Basic')
    return basic_user


@pytest.fixture
def get_or_create_premium_user(db, create_user):
    premium_user = create_user(tier='Premium')
    return premium_user


@pytest.fixture
def get_or_create_enterprise_user(db, create_user):
    enterprise_user = create_user(tier='Enterprise')
    return enterprise_user


@pytest.fixture
def get_or_create_token(db, create_user):
    def get_create(user=None):
        if user is None:
            user = create_user()
        token, _ = Token.objects.get_or_create(user=user)
        return token
    return get_create

@pytest.fixture
def get_or_create_admin_token(db, create_admin_user):
    user = create_admin_user()
    token, _ = Token.objects.get_or_create(user=user)
    return token
