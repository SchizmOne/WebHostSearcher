# Generated by Django 2.2 on 2019-06-18 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getmydata', '0008_auto_20190617_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='scan',
            name='title',
            field=models.TextField(default='Untitled Scan'),
        ),
    ]