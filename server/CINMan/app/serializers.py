from app.models import *
from rest_framework import serializers

from django.apps import apps
from importlib import import_module
import sys

def make_all_fields(model, exclude_fields=()):
    return tuple([f.name for f in model._meta.get_fields() if f.name not in exclude_fields])

class MachineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Machine
		fields = make_all_fields(Machine)

class CINManUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = CINManUser
		fields = make_all_fields(CINManUser)

class MachineUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = MachineUser
		fields = make_all_fields(MachineUser)

class MachineLoginSessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = MachineLoginSession
		fields = make_all_fields(MachineLoginSession)

class LogEntrySerializer(serializers.ModelSerializer):
	class Meta:
		model = LogEntry
		fields = make_all_fields(LogEntry, ("alert",))

