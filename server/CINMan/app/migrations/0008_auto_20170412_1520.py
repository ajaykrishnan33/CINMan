# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_activeloginsession_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='machine',
            field=models.ForeignKey(related_name='machine_alerts', blank=True, to='app.Machine', null=True),
        ),
        migrations.AddField(
            model_name='alert',
            name='user',
            field=models.ForeignKey(related_name='alerts', blank=True, to='app.MachineUser', null=True),
        ),
    ]
