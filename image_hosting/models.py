from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


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
    file_size = models.IntegerField(null=True)
    date_started = models.DateField(auto_now_add=True)
    last_edited = models.DateField(auto_now=True)
    image_url = models.ImageField(upload_to='images/', blank=False, null=False)
    image_thumbnail200 = ImageSpecField(source='image_url', processors=[ResizeToFill(100, 200)], format='JPEG', options={'quality': 60})
    image_thumbnail400 = ImageSpecField(source='image_url', processors=[ResizeToFill(200, 400)], format='JPEG', options={'quality': 60})

    def __str__(self):
        return self.name
