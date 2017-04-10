# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='cpu_speed',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='harddisk_capacity',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='harddisk_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='motherboard_description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='ram_description',
            field=models.TextField(null=True, blank=True),
        ),
    ]
