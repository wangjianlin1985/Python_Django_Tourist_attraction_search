from django.contrib import admin
from apps.ScenicType.models import ScenicType

# Register your models here.

admin.site.register(ScenicType,admin.ModelAdmin)