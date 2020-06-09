from django.shortcuts import render
from icmpscan.scripts.pyping import icmp_scanner
from icmpscan.scripts.tcp_scanner import multiprocess_tcp_scanner_for_ip
from getmydata.models import HomeHost, Scan
from .models import ICMPScan, TCPScan
import ipaddress
import time


# Create your views here.
def index(request):

    current_scan = Scan.objects.last()

    icmp_scans = ICMPScan.objects.filter(scan=current_scan).order_by("ip_address")
    tcp_scans = TCPScan.objects.filter(scan=current_scan).order_by("ip_address")

    if icmp_scans or tcp_scans:
        return render(request, 'icmpscan_html/icmpscan.html', {'icmp_scans': icmp_scans,
                                                               'tcp_scans': tcp_scans,
                                                               'current_scan': current_scan})

    current_host = HomeHost.objects.last()
    network = ipaddress.ip_network(current_host.network_address)

    start_time = time.monotonic()
    icmp_ip_list = icmp_scanner(network)
    stop_time = time.monotonic()

    time_of_icmp = stop_time - start_time
    time_of_icmp = round(time_of_icmp, 2)

    print("ICMP Scan has completed in {} seconds.".format(time_of_icmp))

    current_scan.icmp_scan_time = time_of_icmp
    current_scan.save()

    icmp_scans_list = list()

    for ip in icmp_ip_list:

        icmp_scan = ICMPScan(scan=current_scan, ip_address=ip)
        icmp_scan.save()

        icmp_scans_list.append(icmp_scan)

    start_time = time.monotonic()
    tcp_ip_list = multiprocess_tcp_scanner_for_ip(network)
    stop_time = time.monotonic()

    time_of_tcp = stop_time - start_time
    time_of_tcp = round(time_of_tcp, 2)

    print("TCP Scan has completed in {} seconds.".format(time_of_tcp))

    current_scan.tcp_scan_time = time_of_tcp
    current_scan.save()

    tcp_scans_list = list()

    for ip in tcp_ip_list:

        tcp_scan = TCPScan(scan=current_scan, ip_address=ip)
        tcp_scan.save()

        tcp_scans_list.append(tcp_scan)

    icmp_scans = ICMPScan.objects.filter(scan=current_scan).order_by("ip_address")
    tcp_scans = TCPScan.objects.filter(scan=current_scan).order_by("ip_address")

    return render(request, 'icmpscan_html/icmpscan.html', {'icmp_scans': icmp_scans,
                                                           'tcp_scans': tcp_scans,
                                                           'current_scan': current_scan})
