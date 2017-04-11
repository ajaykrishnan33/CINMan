from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Machine)
admin.site.register(LogEntry)
admin.site.register(Alert)
admin.site.register(MachineUser)
admin.site.register(ActiveLoginSession)
admin.site.register(MachineLoginSession)
admin.site.register(CINManUser)