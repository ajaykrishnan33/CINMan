# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20170410_0521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machineuser',
            name='user',
        ),
        migrations.AddField(
            model_name='alert',
            name='text',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='machine',
            name='host_name',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='machineloginsession',
            name='ip_address',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='machineuser',
            name='username',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='log_entry_type',
            field=models.IntegerField(choices=[(1, b'auth.log'), (2, b'kern.log'), (3, b'daemon.log'), (4, b'dpkg.log'), (5, b'boot.log'), (8, b'lastlog'), (9, b'wtmp'), (10, b'peripherals')]),
        ),
    ]
