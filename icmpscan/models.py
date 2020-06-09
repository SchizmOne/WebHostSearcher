from django.db import models
from getmydata.models import Scan

# Create your models here.


class ICMPScan(models.Model):

    # Внешний ключ на номер сканирования.
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, default=Scan.DEFAULT_PK)

    # Полученный IP-адрес.
    ip_address = models.CharField(max_length=17, default="0.0.0.0")

    def __str__(self):

        return self.ip_address


class TCPScan(models.Model):

    # Внешний ключ на номер сканирования.
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, default=Scan.DEFAULT_PK)

    # Полученный IP-адрес.
    ip_address = models.CharField(max_length=17, default="0.0.0.0")

    def __str__(self):

        return self.ip_address
