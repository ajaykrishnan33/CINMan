# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20170411_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='last_active_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
