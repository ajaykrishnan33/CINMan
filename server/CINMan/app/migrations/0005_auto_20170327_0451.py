# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170327_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='cpu_description',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='cpu_speed',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='harddisk_capacity',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='harddisk_description',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='ip_address',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='kernel_version',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='mac_address',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='motherboard_description',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='os_distro',
            field=models.IntegerField(blank=True, null=True, choices=[(1, b'Ubuntu'), (2, b'RedHat')]),
        ),
        migrations.AlterField(
            model_name='machine',
            name='ram_capacity',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='ram_description',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
