# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alert_type', models.IntegerField(choices=[(1, b'Severe'), (2, b'Mild')])),
            ],
        ),
        migrations.CreateModel(
            name='CINManUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('primary_mail', models.CharField(max_length=100)),
                ('secondary_mail', models.CharField(max_length=100)),
                ('mobile_number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('log_entry_type', models.IntegerField(choices=[(1, b'General message and system related logs'), (2, b'Authentication logs'), (3, b'Kernel logs'), (4, b'Mail server logs'), (5, b'System boot log'), (6, b'MySQL database server log file'), (7, b'Authentication log'), (8, b'Login records'), (9, b'apt'), (10, b'dpkg')])),
                ('text', models.CharField(max_length=1000)),
                ('severity', models.IntegerField(choices=[(1, b'Severe'), (2, b'Mild')])),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.CharField(max_length=20)),
                ('mac_address', models.CharField(max_length=20)),
                ('address_width', models.IntegerField(default=1, choices=[(1, b'64-bit'), (2, b'32-bit')])),
                ('ram_capacity', models.IntegerField()),
                ('ram_description', models.CharField(max_length=100)),
                ('cpu_speed', models.IntegerField()),
                ('cpu_description', models.CharField(max_length=100)),
                ('harddisk_capacity', models.IntegerField()),
                ('harddisk_description', models.CharField(max_length=100)),
                ('motherboard_description', models.CharField(max_length=100)),
                ('os_distro', models.IntegerField(choices=[(1, b'Ubuntu'), (2, b'RedHat')])),
                ('kernel_version', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MachineLoginSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_time', models.DateTimeField()),
                ('logout_time', models.DateTimeField()),
                ('data_downloaded', models.IntegerField()),
                ('data_uploaded', models.IntegerField()),
                ('machine', models.ForeignKey(related_name='login_sessions', to='app.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='MachineUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=20)),
                ('last_logged_in_date', models.DateTimeField()),
                ('last_failed_login_date', models.DateTimeField()),
                ('failed_login_count', models.IntegerField()),
                ('suspicious_activity_count', models.IntegerField()),
                ('number_of_simultaneous_logins', models.IntegerField()),
                ('currently_logged', models.BooleanField(default=False)),
                ('last_logged_in_machine', models.ForeignKey(related_name='last_logged_in_users', to='app.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Peripheral',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(choices=[(1, b'Mouse'), (2, b'Keyboard'), (3, b'Speaker')])),
                ('model', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('machine', models.ForeignKey(related_name='peripherals', to='app.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('software_type', models.IntegerField(choices=[(1, b'System Softwares'), (2, b'Application Softwares')])),
                ('sudo_needed', models.BooleanField(default=False)),
                ('version', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='SoftwareInstallation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_used_date', models.DateTimeField()),
                ('last_user', models.ForeignKey(related_name='softwares_used_last', to='app.MachineUser')),
                ('machine', models.ForeignKey(related_name='software_installations', to='app.Machine')),
                ('software', models.ForeignKey(related_name='installed_machines', to='app.Software')),
            ],
        ),
        migrations.AddField(
            model_name='software',
            name='machine',
            field=models.ManyToManyField(related_name='installed_softwares', through='app.SoftwareInstallation', to='app.Machine'),
        ),
        migrations.AddField(
            model_name='machineloginsession',
            name='user',
            field=models.ForeignKey(related_name='login_sessions', to='app.MachineUser'),
        ),
        migrations.AddField(
            model_name='logentry',
            name='machine',
            field=models.ForeignKey(related_name='machine_logs', to='app.Machine'),
        ),
        migrations.AddField(
            model_name='alert',
            name='log_entry',
            field=models.OneToOneField(related_name='alert', null=True, blank=True, to='app.LogEntry'),
        ),
    ]
