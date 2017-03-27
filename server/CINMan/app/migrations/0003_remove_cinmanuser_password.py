# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170327_0405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cinmanuser',
            name='password',
        ),
    ]
