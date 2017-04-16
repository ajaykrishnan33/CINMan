# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170412_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alert',
            name='machine',
        ),
        migrations.AddField(
            model_name='alert',
            name='machines',
            field=models.ManyToManyField(related_name='machine_alerts', to='app.Machine'),
        ),
    ]
