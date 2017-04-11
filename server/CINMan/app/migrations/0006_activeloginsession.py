# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_machine_last_active_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveLoginSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.CharField(max_length=10, null=True, blank=True)),
                ('login_time', models.DateTimeField(null=True, blank=True)),
                ('logout_time', models.DateTimeField(null=True, blank=True)),
                ('data_downloaded', models.IntegerField(null=True, blank=True)),
                ('data_uploaded', models.IntegerField(null=True, blank=True)),
                ('machine', models.ForeignKey(related_name='active_login_sessions', to='app.Machine')),
                ('mls', models.OneToOneField(related_name='active_login', to='app.MachineLoginSession')),
                ('user', models.ForeignKey(related_name='active_login_sessions', to='app.MachineUser')),
            ],
        ),
    ]
