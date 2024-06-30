from django.contrib import admin
from .models import UploadedFile, FileData

# Register your models here.

admin.site.register(UploadedFile)
admin.site.register(FileData)