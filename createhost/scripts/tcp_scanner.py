# -*- coding: utf-8 -*-
import socket
from .ports import get_tcp_ports
from multiprocessing import Process
from multiprocessing import Queue


def tcp_searcher(ip_address, ports):

    available_ports = dict()

    for port_num in ports.keys():
        sock = socket.socket()
        sock.settimeout(2)

        # Начинаем перебирать порты на IP-адресе.
        try:
            # Если подключение прошло успешно, то добавляем порт
            # в список доступных.
            sock.connect((ip_address, port_num))
            sock.close()
            available_ports[port_num] = ports.get(port_num)

        except ConnectionRefusedError:
            # Если возникла следующая ошибка, то по адресу есть
            # реальный хост, но порт закрыт. Тогда просто
            # перебираем остальные порты.
            continue

        except OSError:
            # Если возникла следующая ошибка, то по адресу
            # возможно есть хост, но либо он уже вышел из
            # сети, либо недоступен. Тогда прекращаем перебор
            # и возвращаем пустое значение.
            return None

        except socket.timeout:
            # Аналогичный случай с OSError.
            return None

    return available_ports


def tcp_scanner(host, results):
    ports = get_tcp_ports()

    available_ports_in_host = tcp_searcher(host.ip_address, ports)

    if available_ports_in_host is None:
        print("\nHost is not up or unreachable.\n"
              "IP address: %s" % host.ip_address)
        host.set_tcp_status("Host is not up or unreachable.")

        try:
            host.hostname = socket.gethostbyaddr(host.ip_address)[0]
            print("Hostname for {} is {}".format(host.ip_address, host.hostname))
        except socket.herror:
            print("Hostname for {} is unknown.".format(host.ip_address))

        results.put(host)
        print()

    elif len(available_ports_in_host) == 0:
        print("\nHost is up, but TCP ports closed or filtered.\n"
              "IP address: %s" % host.ip_address)
        host.set_tcp_status("Host is up, but TCP ports closed or filtered.")

        try:
            host.hostname = socket.gethostbyaddr(host.ip_address)[0]
            print("Hostname for {} is {}".format(host.ip_address, host.hostname))
        except socket.herror:
            print("Hostname for {} is unknown.".format(host.ip_address))

        results.put(host)
        print()
            
    else:
        print("\nHost is up.\n"
              "IP address: %s" % host.ip_address)
        host.set_tcp_status("Host is up.")
        host.set_tcp_ports(available_ports_in_host)

        try:
            host.hostname = socket.gethostbyaddr(host.ip_address)[0]
            print("Hostname for {} is {}".format(host.ip_address, host.hostname))
        except socket.herror:
            print("Hostname for {} is unknown.".format(host.ip_address))

        results.put(host)

        for port_number in available_ports_in_host:
            print(port_number, available_ports_in_host.get(port_number), sep="\t")
            print()


def multiprocess_tcp_scanner(list_of_hosts):

    processes = []
    results = Queue()

    for host in list_of_hosts:
        proc = Process(target=tcp_scanner, args=(host, results))
        processes.append(proc)
        proc.start()

    for proc in processes:
        proc.join()

    list_of_hosts_new = list()

    while not results.empty():
        host = results.get()
        list_of_hosts_new.append(host)

    return list_of_hosts_new


def tcp_scanner_for_ip(ip, results):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    # Начинаем перебирать порты на IP-адресе.
    try:
        # Если подключение прошло успешно, то добавляем порт
        # в список доступных.
        sock.connect((ip, 80))
        #sock.shutdown(2)
        sock.close()
        print("Valid IP:", ip)
        results.put(ip)

    except ConnectionRefusedError:
        # Если возникла следующая ошибка, то по адресу есть
        # реальный хост, но порт закрыт. Тогда просто
        # перебираем остальные порты.
        print("Valid IP:", ip)
        results.put(ip)

    except OSError:
        # Если возникла следующая ошибка, то по адресу
        # возможно есть хост, но либо он уже вышел из
        # сети, либо недоступен. Тогда прекращаем перебор
        # и возвращаем пустое значение.
        pass

    except socket.timeout:
        # Аналогичный случай с OSError.
        pass


def multiprocess_tcp_scanner_for_ip(network):

    network_address = network.network_address
    broadcast = network.broadcast_address
    ip_list = list()
    processes = []
    results = Queue()

    for ip4addr in network:
        if (ip4addr != network_address) and (ip4addr != broadcast):
            ip = str(ip4addr)
            proc = Process(target=tcp_scanner_for_ip, args=(ip, results))
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
