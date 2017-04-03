# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20170402_2212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='peripheral',
            old_name='machine',
            new_name='ip_address',
        ),
    ]
