from django.contrib import admin

# Register your models here.

from .models import HomeHost, Scan

admin.site.register(HomeHost)
admin.site.register(Scan)
