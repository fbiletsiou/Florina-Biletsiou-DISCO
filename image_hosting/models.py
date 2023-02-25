import random
import string
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


def get_thumb_image_path():
    path = "C:\\Users\\FB\\Documents\\Florina-Biletsiou-DISCO-test\\media\\CACHE\\images\\test_thum"
    return path


def randomString(stringLength=20):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class User(AbstractUser):
    """
    Customization of the User object in order to include the tier field.
    """
    class UserTiers(models.TextChoices):
        BASIC = "Basic"
        PREMIUM = "Premium"
        ENTERPRISE = "Enterprise"

    tier = models.CharField(max_length=12, choices=UserTiers.choices, default=UserTiers.BASIC)


class UploadedFile(models.Model):
    """
    File that users upload and own.
    """
    class ValidFileFormat(models.TextChoices):
        PNG = "PNG"
        JPEG = "JPEG"

    name = models.CharField(max_length=50, blank=False, null=False)
    created_by = models.ForeignKey(User,  related_name='images', on_delete=models.CASCADE)
    file_format = models.CharField(max_length=5, default=ValidFileFormat.PNG, choices=ValidFileFormat.choices)
    date_started = models.DateField(auto_now_add=True)
    last_edited = models.DateField(auto_now=True)
    image_url = models.ImageField(upload_to='images/', blank=False, null=False)
    image_thumbnail200 = ImageSpecField(source='image_url', processors=[ResizeToFill(200, 200)], format='JPEG', options={'quality': 60})
    image_thumbnail400 = ImageSpecField(source='image_url', processors=[ResizeToFill(400, 400)], format='JPEG', options={'quality': 60})

    def __str__(self):
        return self.name


class TempUrl(models.Model):
    user = models.ForeignKey(User, related_name='expiry_links', on_delete=models.CASCADE)
    related_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiry_date = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = randomString(stringLength=20)
        return super(TempUrl, self).save(*args, **kwargs)

    def __str__(self):
        return f'for file: {self.related_file} - token: {self.token} - expires: {self.expiry_date}'