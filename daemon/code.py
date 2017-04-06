import os
import sys
import time
import json
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
		print notif
	time.sleep(delay)
