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

	TYPE_CHOICES = (
		#think of types'
  (1, "System Softwares"),
  (2, "Application Softwares");
	)

	machine = models.ManyToManyField(Machine, null=False, blank=False, through=SoftwareInstallation, related_name="installed_softwares")
	#type = models.IntegerField(choices=TYPE_CHOICES)
	sudo_needed = models.BooleanField(default=False)
	version = models.CharField(max_length=200)
  name = models.CharField(max_length=300)

class SoftwareInstallation(models.Model):
  
  machine = models.ForeignKey(Machine, related_name="software_installations")
  software = models.ForeignKey(Software, related_name="installed_machines")
  last_used_date = models.DateTimeField()
	last_user = models.ForeignKey(MachineUser, related_name="softwares_used_last")  
    
class Alert(models.Model):
	
	ALERT_NATURE = (
    (1, "Severe")
    (2, "Mild")
	)
  
  log_entry = models.OneToOneField(LogEntry, null=True, blank=True, related_name="alert")
  alert_type = models.IntegerField(choices=ALERT_NATURE)

class LogEntry(models.Model):
  
	TYPE_CHOICES = (
    (1, "General message and system related logs"),
    (2, "Authentication logs"),
    (3, "Kernel logs"),
    (4, "Mail server logs"),
    (5, "System boot log"),
    (6, "MySQL database server log file"),
    (7, "Authentication log");
    (8, "Login records");
    (9, "apt"),
    (10,"dpkg");
    
  )
  
  SEVERITY_CHOICES = (
    (1, "Severe")
    (2, "Mild")
	)
  
  machine = models.ForeignKey(Machine, null=False, blank=False, related_name="machine_logs")
  timestamp = models.DateTimeField(auto_now_add=True)
  type = models.IntegerField(choices=TYPE_CHOICES)
  text = models.CharField(max_length=1000)
  severity = models.IntegerField(choices=SEVERITY_CHOICES)
  

class CINManUser(models.Model): #Admin
  
  username= models.CharField(max_length=20)
  password=models.CharField(max_length=20)
  primary_mail=models.CharField(max_length=100)
  secondary_mail=models.CharField(max_length=100)
  mobile_number= models.IntegerField();
  
      
class MachineUser(models.Model):
  
  username = models.CharField(max_length=20)   
  last_logged_in_date = models.DateTimeField()
  last_logged_in_machine = models.ForeignKey(Machine, null=False, blank=False, related_name="last_logged_in_users")
  last_failed_login_date = models.DateTimeField()
  failed_login_count = models.IntegerField()
  suspicious_activity_count = models.IntegerField()
  number_of_simultaneous_logins = models.IntegerField()
