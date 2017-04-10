import subprocess
import requests
import netifaces as ni
import datetime
import json
import os
import sys
import time

machineid = 2
ipaddr = ni.ifaddresses("wlan0")[2][0]['addr']

headers = {"Authorization" : "Token 3d7441c3bc2a224b1091c81ec7c152464aadc54c"}

SERVER_URL = "http://localhost:5000/app/logentry/"
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
		r = requests.post(SERVER_URL, data={"log_entry_type":2, "text":notif, "machine":machineid}, headers=headers)
	time.sleep(delay)
	