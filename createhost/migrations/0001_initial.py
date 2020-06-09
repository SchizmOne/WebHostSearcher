# Generated by Django 2.2 on 2019-06-19 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('getmydata', '0011_scan_tcp_scan_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(default='0.0.0.0', max_length=17)),
                ('mac_address', models.CharField(default='Unknown MAC Address', max_length=25)),
                ('company', models.TextField(default='Unknown Company')),
                ('status', models.TextField(default='Unknown Device')),
                ('tcp_status', models.TextField(default='Unknown TCP Status')),
                ('hostname', models.CharField(default='Unknown Hostname', max_length=30)),
                ('sysdescr', models.TextField(default='Unknown System Description')),
                ('scan', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='getmydata.Scan')),
            ],
        ),
        migrations.CreateModel(
            name='TCPPort',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('port_number', models.IntegerField(default=0)),
                ('port_value', models.CharField(default='Unknown Port', max_length=30)),
                ('host', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='createhost.Host')),
            ],
        ),
    ]
