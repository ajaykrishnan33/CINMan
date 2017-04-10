#script to run in background of Client daemon
#Collects os,ram,disc,cpu,network,user,peripherals and software info
#output is json to be sent to server by POST

import os
import time
import json
import commands
import requests

headers = {"Authorization" : "Token 3d7441c3bc2a224b1091c81ec7c152464aadc54c"}
SERVER_URL = "http://localhost:5000/app/machine/"

def get_system_info():
	data = []
	kernel_name = ""
	node_hostname = ""
	kernel_release = ""
	machine_hardware = ""
	processor = ""
	hardware_platform = ""
	operating_system = ""
	mem_total = ""
	mem_available  = ""
	vendor_id = ""
	model_name = ""
	cpu_speed = ""
	cache_size = ""
	processors = ""
	cores_per_processor = ""
	disk_size = ""
	disk_used = ""
	disk_available = ""
	ip_addr = ""
	mac_addr = ""
	users = []
	peripherals_desc = ""
	softwares = []
	software_versions = []
	# try:
	kernel_name = commands.getstatusoutput("uname -s")[1]
	node_hostname = commands.getstatusoutput("uname -n")[1]
	kernel_release = commands.getstatusoutput("uname -r")[1]
	machine_hardware = commands.getstatusoutput("uname -m")[1]
	processor = commands.getstatusoutput("uname -p")[1]
	hardware_platform = commands.getstatusoutput("uname -i")[1]
	operating_system = commands.getstatusoutput("uname -o")[1]
	ramstuff = commands.getstatusoutput("cat /proc/meminfo")
	mem_total = ramstuff[1].split('\n')[0].split(' ')[7]+ramstuff[1].split('\n')[0].split(' ')[8]
	mem_available = ramstuff[1].split('\n')[1].split(' ')[9]+ramstuff[1].split('\n')[1].split(' ')[10]
	cpustuff = commands.getstatusoutput("cat /proc/cpuinfo")
	vendor_id = cpustuff[1].split('\n')[1].split(' ')[1]
	model_name = cpustuff[1].split('\n')[4].split(' ')[2]
	cpu_speed = cpustuff[1].split('\n')[7].split(' ')[2]+'MHz'
	cache_size = cpustuff[1].split('\n')[8].split(' ')[2]+cpustuff[1].split('\n')[8].split(' ')[3]
	processors = cpustuff[1].split('\n')[10].split(' ')[1]
	cores_per_processor = cpustuff[1].split('\n')[12].split(' ')[2]
	diskstuff = commands.getstatusoutput("df -h --total")
	diskstuff = diskstuff[1].split("total")[1].strip()
	diskstuff = [d.strip() for d in diskstuff.split("G")]
	disk_size = diskstuff[0]
	disk_used = diskstuff[1]
	disk_available = diskstuff[2]
	networkstuff = commands.getstatusoutput("/sbin/ifconfig")
	ns = networkstuff[1].split("wlan0")[1].strip()
	ip_addr = ns.split("inet addr:")[1].strip().split(" ")[0]
	mac_addr = ns.split("HWaddr")[1].strip().split(" ")[0]
	userstuff = commands.getstatusoutput("who -q")
	# for i in range(0,len(userstuff[1].split('\n'))-1):
	# 	users.append(userstuff[1].split('\n')[i])
	# peripherals_desc = commands.getstatusoutput("hwinfo --short")[1]	

	payload = {
		"kernel_version" : kernel_name+kernel_release,
		"ip_address" : ip_addr,
		"ram_capacity" : int(mem_total)/1000,
		"mac_address" : mac_addr,
		"cpu_speed" : float(cpu_speed[0:-3])/1000,
		"harddisk_capacity": float(disk_size),
		"harddisk_description" : json.dumps({"size":disk_size, "used":disk_used, "available":disk_available})
	}

	return payload

payload = get_system_info()
r = requests.get(SERVER_URL+"?mac_address="+payload["mac_address"], headers=headers)
res = r.json()
if len(res)==0:
	r = requests.post(SERVER_URL, data=payload, headers=headers)
	a = r.json()
	machine_id = a["id"]
else:
	machine_id = res[0]["id"]

while True:
	payload = get_system_info()
	r = requests.put(SERVER_URL+str(machine_id)+"/", data=payload, headers=headers)
	time.sleep(10)
