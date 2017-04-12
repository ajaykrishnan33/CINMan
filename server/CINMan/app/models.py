from django.db import models
from django.contrib.auth.models import User
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
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

    ip_address = models.CharField(max_length=20, null=True, blank=True)
    host_name = models.CharField(max_length=100, null=True, blank=True)
    mac_address = models.CharField(max_length=20, null=True, blank=True)
    address_width = models.IntegerField(choices=ADDRESS_WIDTH_CHOICES, default=1)
    ram_capacity = models.IntegerField(null=True, blank=True); ## in MBs
    ram_description = models.TextField(null=True, blank=True)
    cpu_speed = models.FloatField(null=True, blank=True); ## in GHz
    cpu_description = models.CharField(max_length=100, null=True, blank=True)
    harddisk_capacity = models.FloatField(null=True, blank=True); ## in GBs
    harddisk_description = models.TextField(null=True, blank=True)
    motherboard_description = models.TextField(null=True, blank=True)
    os_distro = models.IntegerField(choices=OS_CHOICES, null=True, blank=True)
    kernel_version = models.CharField(max_length=30, null=True, blank=True)
    active = models.BooleanField(default=False)
    last_active_at = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.host_name + "(" + self.ip_address+")"

    def save(self,*args,**kwargs):
        redis_publisher = RedisPublisher(facility='foobar', broadcast=True)
        message = RedisMessage("Machine")
        # and somewhere else
        redis_publisher.publish_message(message)
        super(Machine, self).save(*args, **kwargs)

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
        (1, "System Softwares"),
        (2, "Application Softwares")
    )
    machine = models.ManyToManyField(Machine, null=False, blank=False, through='SoftwareInstallation', related_name="installed_softwares")
    software_type = models.IntegerField(choices=TYPE_CHOICES)
    sudo_needed = models.BooleanField(default=False)
    version = models.CharField(max_length=200)
    name = models.CharField(max_length=300)

    def __unicode__(self):
        return self.name


class SoftwareInstallation(models.Model):
  
    machine = models.ForeignKey(Machine, related_name="software_installations")
    software = models.ForeignKey(Software, related_name="installed_machines")
    last_used_date = models.DateTimeField()
    last_user = models.ForeignKey('MachineUser', related_name="softwares_used_last")  
    
class Alert(models.Model):
    ALERT_NATURE = (
        (1, "Severe"),
        (2, "Mild")
    )
    log_entry = models.OneToOneField('LogEntry', null=True, blank=True, related_name="alert")
    alert_type = models.IntegerField(choices=ALERT_NATURE)
    text = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.text

    def save(self,*args,**kwargs):
        redis_publisher = RedisPublisher(facility='foobar', broadcast=True)
        message = RedisMessage("Alert:"+self.text)
        # and somewhere else
        redis_publisher.publish_message(message)
        super(Alert, self).save(*args, **kwargs)

class LogEntry(models.Model):
    TYPE_CHOICES = (
        (1, "auth.log"),
        (2, "kern.log"),
        (3, "daemon.log"),
        (4, "dpkg.log"),
        (5, "boot.log"),
        (8, "lastlog"),
        (9, "wtmp"),
        (10, "peripherals")
    )

    SEVERITY_CHOICES = (
        (1, "Severe"),
        (2, "Mild")
    )
  
    machine = models.ForeignKey(Machine, null=False, blank=False, related_name="machine_logs")
    timestamp = models.DateTimeField()
    log_entry_type = models.IntegerField(choices=TYPE_CHOICES)
    text = models.TextField(null=True, blank=True)
    user = models.ForeignKey('MachineUser', null=True, blank=True, related_name="log_entries")
    severity = models.IntegerField(choices=SEVERITY_CHOICES, default=2)

    def __unicode__(self):
        return str(self.log_entry_type) + "(" + self.machine.host_name + ")"
  

class CINManUser(models.Model): #Admin
    
    user = models.ForeignKey(User, related_name="user_profile")  
    fullname = models.CharField(max_length=20)
    primary_mail = models.CharField(max_length=100, null=True, blank=True)
    secondary_mail = models.CharField(max_length=100, null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    
    def __unicode__(self):
        return self.user.username

class MachineLoginSession(models.Model):  
    machine = models.ForeignKey(Machine, related_name="login_sessions")
    user = models.ForeignKey('MachineUser', related_name="login_sessions")
    ip_address = models.CharField(max_length=10, null=True, blank=True)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    data_downloaded = models.IntegerField(null=True, blank=True)
    data_uploaded = models.IntegerField(null=True, blank=True)  

    def __unicode__(self):
        return self.user.username + "(" + self.machine.host_name + ")"

class ActiveLoginSession(models.Model):  
    mls = models.OneToOneField(MachineLoginSession, related_name="active_login")
    machine = models.ForeignKey(Machine, related_name="active_login_sessions")
    user = models.ForeignKey('MachineUser', related_name="active_login_sessions")
    username = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.CharField(max_length=10, null=True, blank=True)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    data_downloaded = models.IntegerField(null=True, blank=True)
    data_uploaded = models.IntegerField(null=True, blank=True)  

    def __unicode__(self):
        return self.user.username + "(" + self.machine.host_name + ")"

  
class MachineUser(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    last_logged_in_date = models.DateTimeField(null=True, blank=True)
    last_logged_in_machine = models.ForeignKey(Machine, null=True, blank=True, related_name="last_logged_in_users")
    last_failed_login_date = models.DateTimeField(null=True, blank=True)
    failed_login_count = models.IntegerField(null=True, blank=True)
    suspicious_activity_count = models.IntegerField(null=True, blank=True)
    number_of_simultaneous_logins = models.IntegerField(default=0)
    currently_logged = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.username
