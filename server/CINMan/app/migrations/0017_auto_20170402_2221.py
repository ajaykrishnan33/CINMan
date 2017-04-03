# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20170402_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machineuser',
            name='user',
            field=models.ForeignKey(related_name='machineuser_profile', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
