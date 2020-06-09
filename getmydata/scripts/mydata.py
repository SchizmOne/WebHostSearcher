# -*- coding: utf-8 -*-
import socket
import os
import platform
import ipaddress
from .getmac import get_mac_address


def create_homehost(ip, netmask):
    """
    Данная функция получает все основные параметры устройства, на
    котором будет запущена основная програма. В дальнейшем, эти
    параметры будут использованы для остального сканирования сети.

    :return
        my_device_data: Данные об устройстве, в виде словаря, формата:
        {'параметр': 'значение'}
        my_network_data: Данные о локальной интернет-сети, формата
        класса ip_network из модуля ipaddress
    """

    # Данные об устройстве в виде словаря, формата
    # {'параметр': 'значение'}
    my_device_data = dict()

    # Получаем тип системы.
    my_os_type = str(os.name)
    my_os_type = my_os_type.upper()
    my_device_data['os_type'] = my_os_type

    # Получаем название ОС вместе с версией.
    my_os_name = platform.system() + " " + platform.release()
    my_device_data['os_name'] = my_os_name

    # Получаем имя устройства, где запущена программа. Если получить
    # имя не удается, то возвращает 'localhost'.
    my_hostname = socket.getfqdn()
    my_device_data['hostname'] = my_hostname

    # Получаем IP-адрес по имени текущего устройства.
    try:
        my_ip_address = socket.gethostbyname(my_hostname)
        my_device_data['ip_address'] = my_ip_address
    except socket.gaierror:
        print("It seems like entered IP address can't be identified by its hostname.\n")
        my_ip_address = ip
        my_device_data['ip_address'] = my_ip_address

    # Получаем его MAC-адрес.
    my_mac_addr = get_mac_address()
    my_device_data['mac_address'] = my_mac_addr

    my_subnet_mask = netmask

    # Получаем объект типа "сеть", складывая текущий IP-адрес устройства
    # и маску подсети. Это даст нам возможность легко перебирать все
    # адреса в диапозоне и получать адрес сети или
    # широковещательный адрес.

    try:
        my_network = ipaddress.ip_network(my_device_data.get('ip_address') + "/" + my_subnet_mask, strict=False)
        my_device_data['network_address'] = my_network
        my_device_data['subnet_mask'] = my_network.netmask
        my_device_data['broadcast_address'] = my_network.broadcast_address
    except ValueError:
        print("It seems like user entered incorrect data in IP or Subnet Mask.")
        exit(-1)

    # Возвращаем всю полученную информацию.
    return my_device_data
