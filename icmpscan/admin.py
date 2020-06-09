from django.contrib import admin

# Register your models here.

from .models import ICMPScan, TCPScan

admin.site.register(ICMPScan)
admin.site.register(TCPScan)
