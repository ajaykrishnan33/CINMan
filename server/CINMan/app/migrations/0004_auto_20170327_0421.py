# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_cinmanuser_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cinmanuser',
            name='mobile_number',
            field=models.CharField(max_length=15, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='cinmanuser',
            name='primary_mail',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='cinmanuser',
            name='secondary_mail',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
