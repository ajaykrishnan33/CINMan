# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20170402_2141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machine',
            name='id',
        ),
        migrations.AlterField(
            model_name='machine',
            name='ip_address',
            field=models.CharField(default=None, max_length=20, serialize=False, primary_key=True),
            preserve_default=False,
        ),
    ]
