# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20170402_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logentry',
            old_name='ip_address',
            new_name='machine',
        ),
        migrations.RenameField(
            model_name='machineloginsession',
            old_name='ip_address',
            new_name='machine',
        ),
        migrations.RenameField(
            model_name='machineuser',
            old_name='ip_address',
            new_name='last_logged_in_machine',
        ),
        migrations.RenameField(
            model_name='peripheral',
            old_name='ip_address',
            new_name='machine',
        ),
        migrations.RenameField(
            model_name='software',
            old_name='ip_address',
            new_name='machine',
        ),
        migrations.RenameField(
            model_name='softwareinstallation',
            old_name='ip_address',
            new_name='machine',
        ),
        migrations.AddField(
            model_name='machine',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=None, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='machine',
            name='ip_address',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
