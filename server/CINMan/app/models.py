from django.db import models

# Create your models here.

class Machine(models.Model):

	ADDRESS_WIDTH_CHOICES = (
		(1, '64-bit'),
		(2, '32-bit')
	)

	OS_CHOICES = (
		(1, 'Ubuntu'),
		(2, 'RedHat'),
		## add more here
	)

	ip_address = models.CharField(max_length=20)
	mac_address = models.CharField(max_length=20)
	address_width = models.IntergerField(choices=ADDRESS_WIDTH_CHOICES, default=1)
	ram_capacity = models.IntegerField(); ## in MBs
	ram_description = models.CharField(max_length=100)
	cpu_speed = models.IntegerField(); ## in GHz
	cpu_description = models.CharField(max_length=100)
	harddisk_capacity = models.IntegerField(); ## in GBs
	harddisk_description = models.CharField(max_length=100)
	motherboard_description = models.CharField(max_length=100)
	os_distro = models.IntegerField(choices=OS_CHOICES)
	kernel_version = models.CharField(max_length=20)

class Peripheral(models.Model):

	TYPE_CHOICES = (
		(1, "Mouse"),
		(2, "Keyboard"),
		(3, "Speaker")
	)

	machine = models.ForeignKey(Machine, null=False, blank=False, related_name="peripherals")
	type = models.IntegerField(choices=TYPE_CHOICES)
	model = models.CharField(max_length=100)
	description = models.CharField(max_length=200)

class Software(models.Model):
	pass

class Alert(models.Model):
	pass

class LogEntry(models.Model):
	pass

class CINManUser(models.Model):
	pass
