from django.urls import include, path
from django.views.generic import ListView, DetailView

from getmydata.models import Scan
from . import views

urlpatterns = [
    path('', ListView.as_view(queryset=Scan.objects.all().order_by("-time"),
                              template_name="result_html/scans.html")),
    path('<int:pk>/', views.scan_detail_view, name='scan-detail'),
    path('<int:pk>/<int:pk2>', views.host_detail_view, name='host-detail'),
    path('del-<int:pk>/', views.delete_host, name='delete-scan'),
]
