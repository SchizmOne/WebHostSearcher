from django.contrib import admin

# Register your models here.

from .models import Host, TCPPort

admin.site.register(Host)
admin.site.register(TCPPort)
