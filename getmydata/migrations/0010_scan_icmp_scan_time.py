# Generated by Django 2.2 on 2019-06-18 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getmydata', '0009_scan_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='icmp_scan_time',
            field=models.FloatField(default=0.0),
        ),
    ]
