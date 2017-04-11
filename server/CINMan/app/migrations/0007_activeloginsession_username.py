# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_activeloginsession'),
    ]

    operations = [
        migrations.AddField(
            model_name='activeloginsession',
            name='username',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
