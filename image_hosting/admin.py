from django.contrib import admin

from .models import UploadedFile, User

admin.site.register(User)
admin.site.register(UploadedFile)
