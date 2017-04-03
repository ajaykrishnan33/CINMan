# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170402_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='machineuser',
            old_name='last_logged_in_machine',
            new_name='ip_address',
        ),
    ]
