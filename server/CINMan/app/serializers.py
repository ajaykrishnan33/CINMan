from app.models import *
from rest_framework import serializers

from django.apps import apps
from importlib import import_module
import sys

def make_all_fields(model, exclude_fields=()):
    return tuple([f.name for f in model._meta.get_fields() if f.name not in exclude_fields])

class MachineListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Machine
		fields = (
			"id", "ip_address", "host_name", "mac_address",
			"active", "last_active_at"
		)

class MachineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Machine
		fields = (
			"id", "ip_address", "host_name", "mac_address", "address_width",
			"ram_capacity", "ram_description", "cpu_speed", "cpu_description",
			"harddisk_capacity", "harddisk_description", "kernel_version", "os_distro",
			"active", "last_active_at", "active_login_sessions"
		)
		depth = 1

class CINManUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CINManUser
		fields = make_all_fields(CINManUser)

class MachineUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = MachineUser
		fields = (
			"id", "name", "username", "last_logged_in_date", "last_logged_in_machine", 
			"last_failed_login_date", "currently_logged", "active_login_sessions"
		)
		depth = 1

class MachineLoginSessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = MachineLoginSession
		fields = make_all_fields(MachineLoginSession)

class LogEntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = LogEntry
		fields = make_all_fields(LogEntry, ("alert",))

class AlertSerializer(serializers.ModelSerializer):
	class Meta:
		model = Alert
		fields = (
			"id", "log_entry", "alert_type", "machines", "user", "text"
		)
		depth = 1

