from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from getmydata.models import Scan, HomeHost
from getmydata.scripts.start_scan import get_launch_time
from getmydata.scripts.mydata import create_homehost


def index(request):

    if request.method == 'POST':

        # Для начала получим время запуска.
        launch_time = get_launch_time()

        # Сохраним его в БД как новое сканирование.
        # Автоматически создатся primary key.

        scan_title = request.POST.get("title")

        if scan_title != '':
            scan = Scan(launch_time=launch_time, time=timezone.now(), title=request.POST.get("title"))
        else:
            scan = Scan(launch_time=launch_time, time=timezone.now())
        scan.save()

        # Теперь создадим данные о стартовом хосте.
        ip_address = request.POST.get("ip_address")
        subnet_mask = request.POST.get("subnet_mask")

        home_host_data = create_homehost(ip_address, subnet_mask)

        current_scan = Scan.objects.last()

        print("Device Characteristics:")
        print("OS Type . . . . . . . . . . :", home_host_data.get('os_type'))
        print("Name of OS. . . . . . . . . :", home_host_data.get('os_name'))
        print("Hostname. . . . . . . . . . :", home_host_data.get('hostname'))
        print("IP Address. . . . . . . . . :", home_host_data.get('ip_address'))
        print("MAC Address . . . . . . . . :", home_host_data.get('mac_address'))
        print("Network Address . . . . . . :", home_host_data.get('network_address'))
        print("Subnet Mask . . . . . . . . :", home_host_data.get('subnet_mask'))
        print("Broadcast Address . . . . . :", home_host_data.get('broadcast_address'))

        homehost = HomeHost(scan=current_scan,
                            os_type=home_host_data.get('os_type'),
                            os_name=home_host_data.get('os_name'),
                            hostname=home_host_data.get('hostname'),
                            ip_address=home_host_data.get('ip_address'),
                            mac_address=home_host_data.get('mac_address'),
                            network_address=home_host_data.get('network_address'),
                            subnet_mask=home_host_data.get('subnet_mask'),
                            broadcast_address=home_host_data.get('broadcast_address'))
        homehost.save()

        return render(request, 'getmydata_html/submit_net_data.html', {'scan': current_scan, 'homehost': homehost,})

    else:

        return render(request, 'getmydata_html/input_net_data.html')
