import os

import pytest

from image_hosting.models import User


def get_test_files():
    path = ".\\media\\test_media"
    return [f"{path}\\{file_name}" for file_name in os.listdir(path)]


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


@pytest.mark.last
def test_clean_temp_files():
    files = get_test_files()

    for file in files:
        os.remove(file)

    assert len(get_test_files()) == 0
