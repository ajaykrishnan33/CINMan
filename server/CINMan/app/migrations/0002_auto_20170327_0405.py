# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cinmanuser',
            old_name='username',
            new_name='fullname',
        ),
        migrations.AddField(
            model_name='cinmanuser',
            name='user',
            field=models.ForeignKey(related_name='user_profile', default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
