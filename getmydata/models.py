from django.db import models
from django.utils import timezone

# Create your models here.


class Scan(models.Model):

    DEFAULT_PK = 1

    # Время начала сканирования в читаемом виде.
    launch_time = models.CharField(max_length=30, default="Time of scan is unknown")

    # Время начала сканирования в БД-формате.
    time = models.DateTimeField(default=timezone.now)

    # Название сканирования.
    title = models.TextField(default="Untitled Scan")

    # Время ICMP сканирования.
    icmp_scan_time = models.FloatField(default=0.0)

    # Время TCP сканирования.
    tcp_scan_time = models.FloatField(default=0.0)

    def __str__(self):

        if self.title == "Untitled Scan":

            name = self.title + ' ' + '(' + self.launch_time + ')'
            return name

        else:
            return self.title


class HomeHost(models.Model):

    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, default=Scan.DEFAULT_PK)

    # Тип ОС.
    os_type = models.CharField(max_length=10, default="Unknown OS Type")
    # Название ОС.
    os_name = models.CharField(max_length=25, default="Unknown OS Name")

    # Сетевое имя устройства.
    hostname = models.CharField(max_length=30, default="localhost")
    # IPv4-адрес устройства.
    ip_address = models.CharField(max_length=17, default="127.0.0.1")
    # MAC-адрес устройства.
    mac_address = models.CharField(max_length=25, default="Unknown MAC Address")

    # IPv4-адрес сети.
    network_address = models.CharField(max_length=25, default="127.0.0.0/0")
    # Маска подсети.
    subnet_mask = models.CharField(max_length=17, default="0.0.0.0")
    # Адрес широковещательной расслыки.
    broadcast_address = models.CharField(max_length=17, default="127.0.0.255")

    def __str__(self):
        return self.hostname

