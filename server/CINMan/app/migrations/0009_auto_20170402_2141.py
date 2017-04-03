# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170402_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logentry',
            name='text',
            field=models.TextField(null=True, blank=True),
        ),
    ]
