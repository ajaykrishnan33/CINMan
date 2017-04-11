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

my_ip = nf.ifaddresses("wlan0")[2][0]["addr"]

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
		"logged_in_at":timestamp,
		"pts":pts,
		"ip_addr":ip_addr
	}
	return user

def get_user_info():
	temp = [d.strip() for d in commands.getstatusoutput("who am i")[1].split(" ")]
	current_user = one_user(temp)
	
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
	# userstuff = commands.getstatusoutput("who -q")
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

def maintain_contact(machine_id, headers, SERVER_URL):
	while True:
		payload = {
			"user_info" : get_user_info(),
			"machine_info" : get_system_info()
		}
		r = requests.post(SERVER_URL+"machine/"+str(machine_id)+"/periodic/", data=payload, headers=headers)
		time.sleep(10)
