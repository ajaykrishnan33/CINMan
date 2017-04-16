import subprocess
import requests
# import netifaces as ni
import commands
import datetime
import json

def auth_listener(machineid, headers, SERVER_URL):

	p = subprocess.Popen(['tail', '-n', '0', '-f', '/var/log/auth.log'], stdout=subprocess.PIPE)

	for line in iter(p.stdout.readline, b''):
		x = line.find("authentication failure")
		if x >= 0 and line.find("sudo"):
			timestamp = datetime.datetime.now().isoformat()
			username = commands.getstatusoutput("whoami")[1]
			data = {
				"event" : "auth_failure",
				"user" : username,
				"display" : line
			}
			text = json.dumps(data)
			r = requests.post(SERVER_URL+"logentry/", data={"log_entry_type":1, "text":text, "machine":machineid, "timestamp":timestamp, "username" : username}, headers=headers)
			try:
				print r.json()
			except:
				print r.content

		else:
			x = line.find("incorrect password")
			if x >= 0:
				y = line.split(" incorrect password")[0]
				count = y.split(" ")[-1]
				username = commands.getstatusoutput("whoami")[1]
				timestamp = datetime.datetime.now().isoformat()
				command = line[line.find("COMMAND=") + 8:-1]
				pwd = line[line.find("PWD=") + 4:-1].split(" ")[0]
				data = {
					"event" : "incorrect_password",
					"count" : int(count),
					"pwd" : pwd,
					"command" : command,
					"display" : line
				}
				text = json.dumps(data)
				r = requests.post(SERVER_URL+"logentry/", data={"log_entry_type":1, "text":text, "machine":machineid, "timestamp":timestamp, "username" : username}, headers=headers)
				try:
					print r.json()
				except:
					print r.content

			else:
				x = line.find("COMMAND")
				if x >= 0:
					username = commands.getstatusoutput("whoami")[1]
					timestamp = datetime.datetime.now().isoformat()
					command = line[line.find("COMMAND=") + 8:-1]
					pwd = line[line.find("PWD=") + 4:-1].split(" ")[0]
					data = {
						"event" : "sudo_access",
						"pwd" : pwd,
						"command" : command,
						"display" : line
					}
					text = json.dumps(data)
					r = requests.post(SERVER_URL+"logentry/", data={"log_entry_type":1, "text":text, "machine":machineid, "timestamp":timestamp, "username" : username}, headers=headers)
					try:
						print r.json()
					except:
						print r.content

