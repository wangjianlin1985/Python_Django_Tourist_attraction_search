from django.contrib import admin
from apps.Province.models import Province

# Register your models here.

admin.site.register(Province,admin.ModelAdmin)