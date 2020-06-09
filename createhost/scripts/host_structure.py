# -*- coding: utf-8 -*-
from .getmac import get_mac_address
from .macvendors import get_company


class Host:
    status = "Unknown TCP Status"
    hostname = "Unknown Hostname"
    tcp_ports = "Available TCP ports unknown"
    mac_address = "Unknown MAC Address"
    company = "Unknown Company"
    sysdescr = "Unknown System Description"

    def __init__(self, ipaddress):
        self.ip_address = ipaddress

    def set_tcp_status(self, tcp_stat):
        self.status = tcp_stat

    def set_tcp_ports(self, tcpportnumbers):
        self.tcp_ports = tcpportnumbers

    def set_mac_addr(self, macaddress):
        self.mac_address = macaddress

    def set_company(self, company_data):
        self.company = company_data

    def set_hostname(self, host_name):
        self.hostname = host_name

    def set_sysdecr(self, system_description):
        self.sysdescr = system_description


def create_hosts(list_of_ip):

    list_of_hosts = list()

    for ip in list_of_ip:
        host = Host(ip)
        list_of_hosts.append(host)

    return list_of_hosts


def add_macaddr_to_hosts(list_of_hosts, local_ip):

    print()

    for host in list_of_hosts:

        if host.ip_address != local_ip:
            host_mac_address = get_mac_address(ip=host.ip_address)
        else:
            host_mac_address = get_mac_address()

        print("Host IP:", host.ip_address)

        if host_mac_address is not None:
            host.set_mac_addr(host_mac_address)
            print("Host MAC:", host.mac_address)

            company = get_company(host_mac_address)
            host.set_company(company)
            print(company)

        print()


def add_company_to_hosts(list_of_hosts):

    print()

    for host in list_of_hosts:

        if host.mac_address != 'MAC Address unknown':
            company = get_company(host.mac_address)
            host.set_company(company)

            print("Host IP:", host.ip_address)
            print(host.company)
            print()
