# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_machine_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machineloginsession',
            name='data_downloaded',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machineloginsession',
            name='data_uploaded',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machineloginsession',
            name='login_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machineloginsession',
            name='logout_time',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machineuser',
            name='failed_login_count',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machineuser',
            name='last_failed_login_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machineuser',
            name='last_logged_in_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='machineuser',
            name='last_logged_in_machine',
            field=models.ForeignKey(related_name='last_logged_in_users', blank=True, to='app.Machine', null=True),
        ),
        migrations.AlterField(
            model_name='machineuser',
            name='number_of_simultaneous_logins',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='machineuser',
            name='suspicious_activity_count',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
