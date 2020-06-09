from django.shortcuts import render
from getmydata.models import Scan

# Create your views here.
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the main index.")


def index(request):

    scans = Scan.objects.all()

    return render(request, 'main_html/startpage.html', locals())
