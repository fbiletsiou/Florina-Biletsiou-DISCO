import pytest

# from django.contrib.auth.models import User
from image_hosting.models import User


@pytest.mark.django_db
def test_user_create():
    user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    assert User.objects.count() == 1
    assert user.tier == User.UserTiers.BASIC
