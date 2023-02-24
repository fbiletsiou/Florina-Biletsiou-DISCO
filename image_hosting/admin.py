from django.contrib import admin

from .models import UploadedFile, User, TempUrl

admin.site.register(User)
admin.site.register(UploadedFile)
admin.site.register(TempUrl)
