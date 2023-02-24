import pytest

# from django.contrib.auth.models import User
from image_hosting.models import User


@pytest.mark.django_db
def test_user_create():
    user = User.objects.create_user('testuser', 'test@test.com', 'testpassword')
    assert User.objects.count() == 1
    assert user.tier == User.UserTiers.BASIC


@pytest.mark.django_db
def test_premium_user_create():
    user = User.objects.create_user('premiumuser', 'premium@test.com', 'testpassword', tier='Premium')
    assert User.objects.count() == 1
    assert user.tier == User.UserTiers.PREMIUM


@pytest.mark.django_db
def test_enterprise_user_create():
    user = User.objects.create_user('enterpriseuser', 'entersprise@test.com', 'testpassword', tier='Enterprise')
    assert User.objects.count() == 1
    assert user.tier == User.UserTiers.ENTERPRISE
