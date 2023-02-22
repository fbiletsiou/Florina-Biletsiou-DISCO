import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from image_hosting.models import User, UploadedFile
from image_hosting.serializers import UserSerializer, UploadedFileSerializer


class TestSetUp(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username="tester", first_name="a", last_name="Tester", tier='Premium')
        self.token = Token.objects.create(user=self.admin_user)

        self.image_list_create_url = 'images/'
        self.image_retrieve_update_delete_url = 'images/<int:pk>/'
        self.user_list_url = 'users/'
        self.user_retrieve_url = 'users/<int:pk>/'

        self.test_file_png_attributes = {'name': ' ', 'file_format': UploadedFile.ValidFileFormat.PNG}
        self.test_file_png = UploadedFile.objects.create(**self.test_file_png_attributes)
        self.whitelabel_serializer = UploadedFileSerializer(instance=self.test_file_png)

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
