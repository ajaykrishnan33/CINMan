import subprocess
import requests
# import netifaces as ni
import datetime
import json
import commands

#def peri_listener(machineid, headers, SERVER_URL):

p = subprocess.Popen(['tail', '-n', '0', '-f', '/var/log/kern.log'], stdout=subprocess.PIPE)
flag = False
product = ""
manufac = ""
serial = ""

def auth_listener(machineid, headers, SERVER_URL):
	for line in iter(p.stdout.readline, b''):
		timestamp = datetime.now()
		x = line.find("New USB device found")
		username = commands.getstatusoutput("whoami")[1]
		if x >= 0:
			flag = True
		else:
			x = line.find("USB disconnect")
			if x>=0:
				print("USB disconnected")
				data = {
					"event" : "usb_disconnect",
					"display" : "USB disconnected"
				}
				text = json.dumps(data)
				r = requests.post(SERVER_URL+"logentry/", data={"log_entry_type":10, "text":text, "machine":machineid, "timestamp":timestamp, "username" : username}, headers=headers)
				try:
					print r.json()
				except:
					print r.content
			elif flag:
				x = line.find("Product: ")
				if x>=0:
					product = line.split("Product: ")[1].strip()
				else:
					x = line.find("Manufacturer: ")
					if x>=0:
						manufac = line.split("Manufacturer: ")[1].strip()
					else:
						x = line.find("SerialNumber: ")
						if x>=0:
							serial = line.split("SerialNumber: ")[1].strip()
							print("USB connected")
							print(product)
							print(manufac)
							print(serial)
							flag = False
							data = {
								"event" : "usb_connect",
								"display" : "USB("+product+","+manufac+","+serial+") connected"
							}
							text = json.dumps(data)
							r = requests.post(SERVER_URL+"logentry/", data={"log_entry_type":10, "text":text, "machine":machineid, "timestamp":timestamp, "username" : username}, headers=headers)
							try:
								print r.json()
							except:
								print r.content

