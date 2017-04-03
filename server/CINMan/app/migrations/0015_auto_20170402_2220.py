# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0014_auto_20170402_2217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='machineuser',
            name='username',
        ),
        migrations.AddField(
            model_name='machineuser',
            name='user',
            field=models.ForeignKey(related_name='machineuser_profile', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
