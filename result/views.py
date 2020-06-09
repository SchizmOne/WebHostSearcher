from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from getmydata.models import HomeHost, Scan
from icmpscan.models import ICMPScan, TCPScan
from createhost.models import Host, TCPPort


#class ScanDetailView(DetailView):

    #template_name = 'result_html/scan.html'
    #model = Scan

def scan_detail_view(request, pk):

    try:
        scan_id = Scan.objects.get(pk=pk)
    except Scan.DoesNotExist:
        scan_id = get_object_or_404(Scan, pk=pk)

    homehost = HomeHost.objects.get(scan=scan_id)

    icmp_list = ICMPScan.objects.filter(scan=scan_id).order_by("-ip_address")

    tcp_list = TCPScan.objects.filter(scan=scan_id).order_by("-ip_address")

    hosts = Host.objects.filter(scan=scan_id).order_by("ip_address")

    return render(
        request,
        'result_html/scan.html',
        context={'scan': scan_id,
                 'homehost': homehost,
                 'icmp_scans': icmp_list,
                 'tcp_scans': tcp_list,
                 'hosts': hosts}
    )


def host_detail_view(request, pk, pk2):

    try:
        view_host = Host.objects.get(pk=pk2)
    except Host.DoesNotExist:
        view_host = get_object_or_404(Host, pk=pk2)

    view_scan = Scan.objects.get(pk=pk)

    host_ports = TCPPort.objects.filter(host=view_host)

    return render(request, 'result_html/host.html', context={'host': view_host, 'ports': host_ports, 'scan': view_scan})


def delete_host(request, pk):

    try:
        scan_id = Scan.objects.get(pk=pk)
    except Scan.DoesNotExist:
        scan_id = get_object_or_404(Scan, pk=pk)

    homehost = HomeHost.objects.get(scan=scan_id)

    icmp_list = ICMPScan.objects.filter(scan=scan_id)

    tcp_list = TCPScan.objects.filter(scan=scan_id)

    hosts = Host.objects.filter(scan=scan_id)

    for current_host in hosts:

        tcp_ports = TCPPort.objects.filter(host=current_host)

        if tcp_ports.exists():
            tcp_ports.delete()
            current_host.delete()
        else:
            current_host.delete()

    icmp_list.delete()
    tcp_list.delete()

    homehost.delete()
    scan_id.delete()

    return render(request, 'result_html/scan-del.html')
