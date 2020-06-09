# -*- coding: utf-8 -*-
import socket
import struct
import select
import time
import threading
import os
from multiprocessing import Process
from multiprocessing import Queue

default_timer = time.time

# Взято из /usr/include/linux/icmp.h
ICMP_ECHO_REQUEST = 8  # Код эхо-запроса


def checksum(source_string):
    """
    Расчёт контрольной суммы по алгоритму из ping.c
    """
    sum = 0
    countTo = len(source_string)
    count = 0
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum = sum + thisVal
        count = count + 2

    if countTo < len(source_string):
        sum = sum + ord(source_string[len(source_string) - 1])

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff

    # Меняем порядок байт.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receive_one_ping(my_socket, ID, timeout):
    """
    Получает ping-ответ из сокета.
    """
    timeLeft = timeout
    while True:
        startedSelect = default_timer()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = (default_timer() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return

        timeReceived = default_timer()
        recPacket, addr = my_socket.recvfrom(1024)
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )
        # Проверяем, что это эхо-ответ с нашим Id.
        if type != 8 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return


def send_one_ping(my_socket, dest_addr, ID):
    """
    Посылает один пинг по адресу dest_addr.
    """
    dest_addr = socket.gethostbyname(dest_addr)

    # Заголовок состоит из полей: type (8), code (8), checksum (16), id (16), sequence (16)

    my_checksum = 0

    # Создаём пустой заголовок с нулевой контрольной суммой.
    # ID: Идентификатор в Low-endian представлении, bbHHh: сетевой порядок байт.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    bytesInDouble = struct.calcsize("d")
    data = (192 - bytesInDouble) * "Q"
    data = struct.pack("d", default_timer()) + data.encode()

    # Вычисляем контрольную сумму данных с пустым заголовком.
    my_checksum = checksum(header + data)

    # Теперь, когда у нас есть правильная контрольная сумма, мы вставляем ее.
    # Легче всего составить новый заголовок, чем вставить её черновой пакет.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1)
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1))  # Don't know about the 1


def ping(dest_addr, timeout=2, unit="s"):
    """
    Посылает один ping по заданному адресу с таймаутом.

    :param
        dest_addr: Строка. Проверяемый адрес. Например: "192.168.1.1"/"example.com"
        timeout: Целое. Таймаут в секундах. По умолчанию 4.
        unit: Строка. Единицы измерения. По умолчанию: "s" (секунды), "ms" - миллисекунды.

    :return
        Задержка в секунда/миллисекундах, или None при таймауте.
    """
    icmp_protocol = socket.getprotobyname("icmp")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp_protocol)
    my_ID = threading.current_thread().ident & 0xFFFF
    send_one_ping(my_socket, dest_addr, my_ID)
    delay = receive_one_ping(my_socket, my_ID, timeout)  # in seconds
    my_socket.close()
    if delay is None:
        return None
    if unit == "ms":
        delay *= 1000  # in milliseconds
    return delay


def verbose_ping(dest_addr, queue, timeout=2, count=1):
    """
    Посылает pings по заданному адресу и отображает результат

    :param
        dest_addr: Строка. Адрес назаначения. Например "192.168.1.1"/"example.com"
        timeout: Целое. Таймаут в секундах. По умолчанию: 4 секунды.
        count: Целое. Сколько ping посылать. По умолчанию 4.

    :return
        Форматированный вывод на печать.
    """
    for i in range(count):
        # print("ping '{}' ... ".format(dest_addr), end='')
        try:
            delay = ping(dest_addr, timeout)
        except socket.gaierror as e:
            # print("Failed. (socket error: '{}')".format(e))
            break
        if delay is None:
            # print("Timeout > {}s".format(timeout))
            pass
        else:
            delay = delay * 1000
            # print("{}ms".format(int(delay)))
            queue.put(dest_addr)


def pinger(ip, queue):
    icmp = socket.getprotobyname("icmp")
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    proc_id = os.getpid()
    send_one_ping(my_socket, ip, proc_id)
    res = receive_one_ping(my_socket, proc_id, 5)
    if res is not None:
        # print("Valid IP:", ip, "proc id:", proc_id)
        print("Valid IP:", ip)
        queue.put(ip)
    else:
        # print("Not Valid IP:", ip, "proc id:", proc_id)
        pass
    my_socket.close()


def icmp_scanner(network):
    """
    Составляет список хостов.
    :param
        pool_size: Целое. Количество параллельных запусков команды ping
    :return
        Cписок ip-адресов, с которых пришел ответ
    """
    network_address = network.network_address
    broadcast = network.broadcast_address
    ip_list = list()
    processes = []
    results = Queue()

    for ip4addr in network:
        if (ip4addr != network_address) and (ip4addr != broadcast):
            ip = str(ip4addr)
            proc = Process(target=pinger, args=(ip, results))
            processes.append(proc)
            proc.start()
        else:
            continue

    for proc in processes:
        proc.join()

    while not results.empty():
        ip = results.get()
        ip_list.append(ip)

    return ip_list
