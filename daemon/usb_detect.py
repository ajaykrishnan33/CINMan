import subprocess
import requests
import datetime
import json
import os
import sys
import time

def usb_listener(machineid, headers, SERVER_URL):
	disks = 'lsblk -PS | grep "disk" | grep '
	usb = "'"+'TRAN="usb"'+"'" + "> usb_detect" 
	delay=5 #in seconds
	data = {}

	while True:
		disks = 'lsblk -PS | grep "disk" | grep '
		usb = "'"+'TRAN="usb"'+"'" + "> usb_detect" 
		a=os.system(disks+usb)
		if a== 0:
			with open('usb_detect','r') as f:
				d= f.read().replace('\n','')
			vendor = d.split('VENDOR="')[1].split('"')[0]
			model = d.split('MODEL="')[1].split('"')[0]
			data= {"event" : "external usb","vendor" : vendor,"model":model}
			f.close()
			notif=json.dumps(data)
			r = requests.post(SERVER_URL+"logentry/", data={"log_entry_type":10, "text":notif, "machine":machineid}, headers=headers)
		time.sleep(delay)
	