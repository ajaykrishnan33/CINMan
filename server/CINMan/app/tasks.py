from celery import shared_task
from app.models import *
from django.utils import timezone
from datetime import timedelta

@shared_task
def update_active_machines():
	machines = Machine.objects.all()
	curr_time = timezone.now()

	threshold = timedelta(seconds=60)

	print "Updating active machines..."

	for m in machines:
		if m.last_active_at is not None and curr_time - m.last_active_at > threshold:
			m.active = False
			for als in m.active_login_sessions.all():
				als.mls.logout_time = curr_time
				als.mls.save(update_fields=['logout_time'])
			m.active_login_sessions.all().delete()
			m.save(update_fields=['active'])

	print "Checking for multiple logins..."

	users = MachineUser.objects.all()

	for u in users:
	    ipcount = len(set([d.ip_address for d in u.active_login_sessions.all()]))
	    if ipcount>1:
	        a = Alert(alert_type=1, text=u.username+" has logged in from multiple IP addresses.")
	        a.save()