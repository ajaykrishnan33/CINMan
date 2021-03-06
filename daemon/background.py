#script to run in background of Client daemon
#Collects os,ram,disc,cpu,network,user,peripherals and software info
#output is json to be sent to server by POST

import os
import time
import json
import commands
import requests
import datetime
import netifaces as nf

default_interface = commands.getstatusoutput("route | grep '^default' | grep -o '[^ ]*$'")[1]

my_ip = nf.ifaddresses(default_interface)[2][0]["addr"]

def one_user(temp):
	user_details = []
	for d in temp:
		if len(d)>0:
			user_details.append(d)
	username = user_details[0]
	pts = user_details[1]
	timestamp = datetime.datetime.strptime(user_details[2]+" "+user_details[3], "%Y-%m-%d %H:%M")
	ip_addr = user_details[4].strip()[1:-1]

	if ip_addr == "0:0" or ip_addr == ":0":
		ip_addr = my_ip

	user = {
		"username":username,
		"logged_in_at":timestamp.isoformat(),
		"tty":pts,
		"ip_address":ip_addr
	}
	return user

def get_user_info():
	current_user = {
		"username" : commands.getstatusoutput("whoami")[1]
	}
	
	temp_list = commands.getstatusoutput("who")[1].split("\n")
	all_user_details = []
	for t in temp_list:
		t = t.strip()
		temp = [d.strip() for d in t.split(" ")]
		all_user_details.append(one_user(temp))

	payload = {
		"current_user" : current_user,
		"all_user_details": all_user_details
	}

	return payload

def get_system_info():
	kernel_name = commands.getstatusoutput("uname -s")[1]
	node_hostname = commands.getstatusoutput("uname -n")[1]
	kernel_release = commands.getstatusoutput("uname -r")[1]
	machine_hardware = commands.getstatusoutput("uname -m")[1]
	processor = commands.getstatusoutput("uname -p")[1]
	hardware_platform = commands.getstatusoutput("uname -i")[1]

	ramstuff = commands.getstatusoutput("cat /proc/meminfo")[1]
	ramstuff = ramstuff.split("\n")

	os_distro = commands.getstatusoutput("cat /etc/*-release")[1].strip().split("DISTRIB_DESCRIPTION=")[1].split("\n")[0][1:-1].strip()

	mem_total = ramstuff[0].split(":")[1].strip().split(" ")[0] ## total
	mem_available = ramstuff[2].split(":")[1].strip().split(" ")[0] ## available
	mem_free = ramstuff[1].split(":")[1].strip().split(" ")[0] ## free

	cpustuff = commands.getstatusoutput("cat /proc/cpuinfo")
	vendor_id = cpustuff[1].split('vendor_id')[1].split('\n')[0][2:].strip()
	model_name = cpustuff[1].split('model name')[1].split('\n')[0][2:].strip()
	cpu_speed = cpustuff[1].split('cpu MHz')[1].split('\n')[0][3:].strip()+'MHz'
	cache_size = cpustuff[1].split('cache size')[1].split('\n')[0][2:].strip()
	processors = cpustuff[1].split('siblings')[1].split('\n')[0][2:].strip()
	cores_per_processor = cpustuff[1].split('cpu cores')[1].split('\n')[0][2:].strip()
	diskstuff = commands.getstatusoutput("df -h --total")
	diskstuff = diskstuff[1].split("total")[1].strip()
	diskstuff = [d.strip() for d in diskstuff.split("G")]
	disk_size = diskstuff[0]
	disk_used = diskstuff[1]
	disk_available = diskstuff[2]
	# networkstuff = commands.getstatusoutput("/sbin/ifconfig")
	# ns = networkstuff[1].split("wlan0")[1].strip()
	# ip_addr = ns.split("inet addr:")[1].strip().split(" ")[0]
	# mac_addr = ns.split("HWaddr")[1].strip().split(" ")[0]

	default_interface = commands.getstatusoutput("route | grep '^default' | grep -o '[^ ]*$'")[1]
	ip_addr = nf.ifaddresses(default_interface)[2][0]["addr"]
	mac_addr = nf.ifaddresses(default_interface)[nf.AF_LINK][0]["addr"]

	# userstuff = commands.getstatusoutput("who -q")
	# for i in range(0,len(userstuff[1].split('\n'))-1):
	# 	users.append(userstuff[1].split('\n')[i])
	# peripherals_desc = commands.getstatusoutput("hwinfo --short")[1]	

	payload = {
		"host_name" : node_hostname,
		"os_distro" : os_distro,
		"kernel_version" : kernel_name+kernel_release,
		"ip_address" : ip_addr,
		"ram_capacity" : int(mem_total)/1000,
		"ram_description": json.dumps({"total":mem_total, "available":mem_available, "free":mem_free}),
		"mac_address" : mac_addr,
		"cpu_speed" : float(cpu_speed[0:-3])/1000,
		"harddisk_capacity": float(disk_size),
		"harddisk_description" : json.dumps({"size":disk_size, "used":disk_used, "available":disk_available})
	}

	return payload

def maintain_contact(machine_id, headers, SERVER_URL):
	while True:
		payload = {
			"user_info" : json.dumps(get_user_info()),
			"machine_info" : json.dumps(get_system_info())
		}
		# print payload
		r = requests.post(SERVER_URL+"machine/"+str(machine_id)+"/periodic/", data=payload, headers=headers)

		try:
			x = r.json()
		except:
			print r.content.strip()

		time.sleep(10)
