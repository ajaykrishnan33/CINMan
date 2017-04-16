import subprocess
import requests
# import netifaces as ni
import datetime
import json

# machineid = 1
# ipaddr = ni.ifaddresses("wlan0")[2][0]['addr']

# headers = {"Authorization" : "Token 3d7441c3bc2a224b1091c81ec7c152464aadc54c"}

# SERVER_URL = "http://10.21.187.123:5000/app/logentry/"

def auth_listener(machineid, headers, SERVER_URL):

	p = subprocess.Popen(['tail', '-n', '0', '-f', '/var/log/auth.log'], stdout=subprocess.PIPE)

	for line in iter(p.stdout.readline, b''):
		x = line.find("authentication failure")
		if x >= 0 and line.find("sudo"):
			timestamp = datetime.datetime.strptime(" ".join([line.split(" ")[0]] + line.split(" ")[1:3]), "%b  %d %H:%M:%S").replace(year=datetime.datetime.now().year).isoformat()
			username = line.split("logname=")[1].split(" ")[0]
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
				username = y.split(" ")[-3]
				timestamp = datetime.datetime.strptime(" ".join([line.split(" ")[0]] + line.split(" ")[1:3]), "%b  %d %H:%M:%S").replace(year=datetime.datetime.now().year).isoformat()
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
					username = line.split("sudo:")[1].strip().split(" ")[0]
					print username
					timestamp = datetime.datetime.strptime(" ".join([line.split(" ")[0]] + line.split(" ")[2:4]), "%b  %d %H:%M:%S").replace(year=datetime.datetime.now().year).isoformat()
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

