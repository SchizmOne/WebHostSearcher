# -*- coding: utf-8 -*-
import urllib.request as urllib2
import urllib.error
import json
import codecs
import socket


def get_company(mac_address):
    """
    Данная фунция посылает HTTP запрос на API сайта MacVendors.co,
    который обрабатывает присланный MAC-адрес и возвращает ответ
    с информацией о компании-производителе в формате json.
    :param
        mac_address: Ну, тут все понятно.
    :return:
        company: Информация о компании-производителе.
    """

    # url API сервера MacVendors
    url = "http://macvendors.co/api/"

    # Формируем строку запроса.
    request = urllib2.Request(url+mac_address, headers={'User-Agent': "API Browser"})

    try:
        # Отправляем запрос и сохраняем ответ от сервера.
        response = urllib2.urlopen(request, timeout=5.0)
    except urllib.error.HTTPError:
        company = "Unknown Company"
        return company
    except socket.timeout:
        company = "Unknown Company"
        return company


    # Преобразуем ответ в формат словаря.
    reader = codecs.getreader("utf-8")
    obj = json.load(reader(response))

    # Проверяем, что сервер нашел компанию по MAC-адресу.
    if obj.get('result') != {'error': 'no result'}: 

        company = obj['result']['company']
        return company

    else:
        company = "Unknown Company"
        return company
