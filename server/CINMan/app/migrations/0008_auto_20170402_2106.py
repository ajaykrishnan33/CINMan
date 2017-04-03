# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170327_0836'),
    ]

    operations = [
        migrations.AddField(
            model_name='logentry',
            name='user',
            field=models.ForeignKey(related_name='log_entries', blank=True, to='app.MachineUser', null=True),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='log_entry_type',
            field=models.IntegerField(choices=[(1, b'auth.log'), (2, b'kern.log'), (3, b'daemon.log'), (4, b'dpkg.log'), (5, b'boot.log'), (8, b'lastlog'), (9, b'wtmp')]),
        ),
        migrations.AlterField(
            model_name='logentry',
            name='severity',
            field=models.IntegerField(default=2, choices=[(1, b'Severe'), (2, b'Mild')]),
        ),
    ]
