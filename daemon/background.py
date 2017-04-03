#script to run in background of Client daemon
#Collects os,ram,disc,cpu,network,user,peripherals and software info
#output is json to be sent to server by POST

import os
import time
import simplejson
import commands

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
try:
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
	disk_size = diskstuff[1].split('\n')[11].split(' ')[12]
	disk_used = diskstuff[1].split('\n')[11].split(' ')[14]
	disk_available = diskstuff[1].split('\n')[11].split(' ')[17]
	networkstuff = commands.getstatusoutput("/sbin/ifconfig")
	ip_addr = networkstuff[1].split('\n')[1].split(' ')[9]
	mac_addr = networkstuff[1].split('\n')[2].split(' ')[9]
	userstuff = commands.getstatusoutput("who -q")
	for i in range(0,len(userstuff[1].split('\n'))-1):
		users.append(userstuff[1].split('\n')[i])
	peripherals_desc = commands.getstatusoutput("hwinfo --short")[1]
	softinfo = commands.getstatusoutput("dpkg -l")[1]
	for i in range(5,len(softinfo.split('\n'))):
		softwares.append(softinfo.split('\n')[i].split(' ')[2])
		software_versions.append(softinfo.split('\n')[i].split(' ')[26])
except:
	print("ERROR")


dict1 = {"kernel name" : kernel_name , "node hostname" : node_hostname , "kernel release" : kernel_release , "machine hardware" : machine_hardware , "processor" : processor , "hardware platform" : hardware_platform, "operating system" : operating_system}
dict2 = {"total memory" :mem_total , "available memory" : mem_available}
dict3 = {"vendor id" : vendor_id , "model name" : model_name , "cpu speed" : cpu_speed , "cache size" : cache_size , "processors" : processors , "cores per processor" : cores_per_processor}
dict4 = {"size" : disk_size , "used" : disk_used , "available" : disk_available}
dict5 = {"ip addr" : ip_addr, "mac addr" : mac_addr}
dict6 = {"user list" : users}
dict7 = {"peripherals" : peripherals_desc}
dict8 = {"softwares" : softwares}
data.append(dict1)
data.append(dict2)
data.append(dict3)
data.append(dict4)
data.append(dict5)
data.append(dict6)
data.append(dict7)
data.append(dict8)
data = simplejson.dumps(data)
print(data)