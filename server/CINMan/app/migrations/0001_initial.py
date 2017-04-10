# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('fullname', models.CharField(max_length=20)),
                ('primary_mail', models.CharField(max_length=100, null=True, blank=True)),
                ('secondary_mail', models.CharField(max_length=100, null=True, blank=True)),
                ('mobile_number', models.CharField(max_length=15, null=True, blank=True)),
                ('user', models.ForeignKey(related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('log_entry_type', models.IntegerField(choices=[(1, b'auth.log'), (2, b'kern.log'), (3, b'daemon.log'), (4, b'dpkg.log'), (5, b'boot.log'), (8, b'lastlog'), (9, b'wtmp')])),
                ('text', models.TextField(null=True, blank=True)),
                ('severity', models.IntegerField(default=2, choices=[(1, b'Severe'), (2, b'Mild')])),
            ],
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.CharField(max_length=20, null=True, blank=True)),
                ('mac_address', models.CharField(max_length=20, null=True, blank=True)),
                ('address_width', models.IntegerField(default=1, choices=[(1, b'64-bit'), (2, b'32-bit')])),
                ('ram_capacity', models.IntegerField(null=True, blank=True)),
                ('ram_description', models.CharField(max_length=100, null=True, blank=True)),
                ('cpu_speed', models.IntegerField(null=True, blank=True)),
                ('cpu_description', models.CharField(max_length=100, null=True, blank=True)),
                ('harddisk_capacity', models.IntegerField(null=True, blank=True)),
                ('harddisk_description', models.CharField(max_length=100, null=True, blank=True)),
                ('motherboard_description', models.CharField(max_length=100, null=True, blank=True)),
                ('os_distro', models.IntegerField(blank=True, null=True, choices=[(1, b'Ubuntu'), (2, b'RedHat')])),
                ('kernel_version', models.CharField(max_length=20, null=True, blank=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MachineLoginSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_time', models.DateTimeField(null=True, blank=True)),
                ('logout_time', models.DateTimeField(null=True, blank=True)),
                ('data_downloaded', models.IntegerField(null=True, blank=True)),
                ('data_uploaded', models.IntegerField(null=True, blank=True)),
                ('machine', models.ForeignKey(related_name='login_sessions', to='app.Machine')),
            ],
        ),
        migrations.CreateModel(
            name='MachineUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('last_logged_in_date', models.DateTimeField(null=True, blank=True)),
                ('last_failed_login_date', models.DateTimeField(null=True, blank=True)),
                ('failed_login_count', models.IntegerField(null=True, blank=True)),
                ('suspicious_activity_count', models.IntegerField(null=True, blank=True)),
                ('number_of_simultaneous_logins', models.IntegerField(default=0)),
                ('currently_logged', models.BooleanField(default=False)),
                ('last_logged_in_machine', models.ForeignKey(related_name='last_logged_in_users', blank=True, to='app.Machine', null=True)),
                ('user', models.OneToOneField(related_name='machineuser_profile', to=settings.AUTH_USER_MODEL)),
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
            model_name='logentry',
            name='user',
            field=models.ForeignKey(related_name='log_entries', blank=True, to='app.MachineUser', null=True),
        ),
        migrations.AddField(
            model_name='alert',
            name='log_entry',
            field=models.OneToOneField(related_name='alert', null=True, blank=True, to='app.LogEntry'),
        ),
    ]
