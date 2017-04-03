import os
import time
import simplejson
import commands

authentication_logs=""
kernel_logs=""
boot_logs=""
dpkg_logs=""
dmsg_logs=""
system_logs=""
user_authentication_logs=""

directory="/var/log/"
try:
	authentication_logs=commands.getstatusoutput("cat "+directory+"auth.log")
	kernel_logs=commands.getstatusoutput("cat "+directory+"kern.log")
	boot_logs=commands.getstatusoutput("cat "+directory+"boot.log")
	dpkg_logs=commands.getstatusoutput("cat "+directory+"dpkg.log")
	dmesg_logs=commands.getstatusoutput("cat "+directory+"dmesg")
	system_logs=commands.getstatusoutput("cat "+directory+"sys.log")
	login_records=commands.getstatusoutput("strings "+directory+"wtmp")

except:
	print "Something is wrong"

dictionary={"authentication logs":authentication_logs[1],"kernel logs":kernel_logs[1],"boot logs":boot_logs[1],"dpkg logs":dpkg_logs[1],"dmesg logs":dmesg_logs[1],"system_logs":system_logs[1],
			"login logs": login_records[1]}


for key,value in dictionary.iteritems():
	value = unicode(value, errors='ignore')
	# if key is "login logs":
	# 	print value	


json_file=simplejson.dumps(dictionary)
# print(json_file)