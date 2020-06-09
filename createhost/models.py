from django.db import models
from getmydata.models import Scan

# Create your models here.


class Host(models.Model):

    DEFAULT_PK = 1

    # Номер сканирования.
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE, default=Scan.DEFAULT_PK)

    # IPv4-адрес устройства.
    ip_address = models.CharField(max_length=17, default="0.0.0.0")

    # MAC-адрес устройства.
    mac_address = models.CharField(max_length=25, default="Unknown MAC Address")

    # Компания-производитель устройства.
    company = models.TextField(default="Unknown Company")

    # Общий статус устройства, примечания.
    status = models.TextField(default="Unknown Device")

    # Статус устройства по TCP.
    tcp_status = models.TextField(default="Unknown TCP Status")

    # Сетевое имя устройства.
    hostname = models.CharField(max_length=30, default="Unknown Hostname")

    # Системное описание устройства.
    sysdescr = models.TextField(default="Unknown System Description")

    def __str__(self):

        if self.hostname != "Unknown Hostname":
            return self.hostname
        else:
            return self.ip_address


class TCPPort(models.Model):

    # Номер хоста.
    host = models.ForeignKey(Host, on_delete=models.CASCADE, default=Host.DEFAULT_PK)

    # Номер порта.
    port_number = models.IntegerField(default=0)

    # Назначение порта.
    port_value = models.CharField(max_length=30, default="Unknown Port")

    def __str__(self):

        return str(self.port_number) + ": " + self.port_value
