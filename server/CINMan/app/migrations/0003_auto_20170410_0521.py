# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170410_0500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='kernel_version',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
