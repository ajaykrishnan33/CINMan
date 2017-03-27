# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20170327_0451'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]