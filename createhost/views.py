from django.shortcuts import render
from getmydata.models import Scan, HomeHost
from icmpscan.models import ICMPScan, TCPScan
from django.shortcuts import get_object_or_404
from createhost.scripts.host_structure import *
from createhost.scripts.tcp_scanner import multiprocess_tcp_scanner
from createhost.scripts.snmp_scanner import snmp_scan
from createhost.models import Host, TCPPort

# Create your views here.


def index(request):

    # Вытаскиваем последнее сканирование.
    current_scan = Scan.objects.last()

    list_of_hosts = Host.objects.filter(scan=current_scan).order_by("ip_address")

    if list_of_hosts:
        return render(request, 'createhost_html/hosts.html', {'hosts': list_of_hosts, 'scan': current_scan})

    # Достаем полученные по сканированию результаты по TCP и ICMP
    icmp_list = ICMPScan.objects.filter(scan=current_scan)
    tcp_list = TCPScan.objects.filter(scan=current_scan)

    # Готовим окончательный список адресов.
    ip_list = list()

    for item in icmp_list:
        ip = item.ip_address
        ip_list.append(ip)

    for item in tcp_list:
        ip = item.ip_address
        if ip not in ip_list:
            ip_list.append(ip)

    # Создадим список хостов.
    hosts = create_hosts(ip_list)
    current_host = HomeHost.objects.last()

    add_macaddr_to_hosts(hosts, current_host.ip_address)
    hosts = multiprocess_tcp_scanner(hosts)

    #snmp_scan(hosts)

    for host in hosts:

        if current_host.ip_address != host.ip_address:

            new_host = Host(scan=current_scan,
                            ip_address=host.ip_address,
                            mac_address=host.mac_address,
                            company=host.company,
                            tcp_status=host.status,
                            hostname=host.hostname,
                            sysdescr=host.sysdescr)
            new_host.save()

        else:

            new_host = Host(scan=current_scan,
                            ip_address=host.ip_address,
                            mac_address=host.mac_address,
                            company=host.company,
                            tcp_status=host.status,
                            hostname=current_host.hostname,
                            sysdescr=current_host.os_name)
            new_host.save()

        if host.tcp_ports != "Available TCP ports unknown":

            for port in host.tcp_ports:

                new_port = TCPPort(host=new_host,
                                   port_number=port,
                                   port_value=host.tcp_ports.get(port))
                new_port.save()

    list_of_hosts = Host.objects.filter(scan=current_scan).order_by("ip_address")

    return render(request, 'createhost_html/hosts.html', {'hosts': list_of_hosts, 'scan': current_scan})


def detail_host(request, pk):

    try:
        view_host = Host.objects.get(pk=pk)
    except Host.DoesNotExist:
        view_host = get_object_or_404(Host, pk=pk)

    host_ports = TCPPort.objects.filter(host=view_host)

    return render(request, 'createhost_html/host.html', context={'host': view_host, 'ports': host_ports})





