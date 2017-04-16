import subprocess
import requests
# import netifaces as ni
import datetime
import json
import commands

def dpkg_listener(machineid, headers, SERVER_URL):

	p = subprocess.Popen(['tail', '-n', '0', '-f', '/var/log/dpkg.log'], stdout=subprocess.PIPE)

	for line in iter(p.stdout.readline, b''):

		x = line.find(" install ")
		if x>=0 :
			package_name = line.split(" install ")[1].strip()
			timestamp = datetime.datetime.now().isoformat()
			username = commands.getstatusoutput("whoami")[1]
			data = {
				"event" : "package_install",
				"package" : package_name,
				"user" : username,
				"display" : line
			}
			text = json.dumps(data)
			r = requests.post(SERVER_URL+"logentry/", data={"log_entry_type":4, "text":text, "machine":machineid, "timestamp":timestamp, "username" : username}, headers=headers)
		else:
			line = line.strip()
			x = line.find(" remove ")
			if x>=0 :
				print line
				package_name = line.split(" remove ")[1].strip()
				timestamp = datetime.datetime.now().isoformat()
				username = commands.getstatusoutput("whoami")[1]
				data = {
					"event" : "package_remove",
					"package" : package_name,
					"user" : username,
					"display" : line
				}
				text = json.dumps(data)
				r = requests.post(SERVER_URL+"logentry/", data={"log_entry_type":4, "text":text, "machine":machineid, "timestamp":timestamp, "username" : username}, headers=headers)


		