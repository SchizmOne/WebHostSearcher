# Generated by Django 2.2 on 2019-06-17 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getmydata', '0006_auto_20190614_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='launch_time',
            field=models.CharField(max_length=30),
        ),
    ]
