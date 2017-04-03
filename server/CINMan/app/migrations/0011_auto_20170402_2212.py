# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20170402_2208'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logentry',
            old_name='machine',
            new_name='ip_address',
        ),
        migrations.RenameField(
            model_name='machineloginsession',
            old_name='machine',
            new_name='ip_address',
        ),
        migrations.RenameField(
            model_name='software',
            old_name='machine',
            new_name='ip_address',
        ),
        migrations.RenameField(
            model_name='softwareinstallation',
            old_name='machine',
            new_name='ip_address',
        ),
    ]
