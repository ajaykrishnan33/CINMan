import requests
from background import get_system_info, maintain_contact
from auth_listen import auth_listener
from dpkg_listen import dpkg_listener
from peri_listen import peri_listener
import threading

f = open("config.txt", "r");
config = f.read().split("\n");
headers = {"Authorization" : "Token "+config[0]}
SERVER_URL = config[1]

payload = get_system_info()
r = requests.get(SERVER_URL+"machine/?mac_address="+payload["mac_address"], headers=headers)
res = r.json()
if len(res)==0:
	r = requests.post(SERVER_URL+"machine/", data=payload, headers=headers)
	a = r.json()
	machine_id = a["id"]
else:
	machine_id = res[0]["id"]

t1 = threading.Thread(target=maintain_contact, args=(machine_id, headers, SERVER_URL))
t1.start()
t2 = threading.Thread(target=auth_listener, args=(machine_id, headers, SERVER_URL))
t2.start()
t3 = threading.Thread(target=dpkg_listener, args=(machine_id, headers, SERVER_URL))
t3.start()
t4 = threading.Thread(target=peri_listener, args=(machine_id, headers, SERVER_URL))
t4.start()

while True:
	if not t1.isAlive():
		print "background thread dead"
	if not t2.isAlive():
		print "auth_listener thread dead"
	if not t3.isAlive():
		print "dpkg_listener thread dead"
	if not t4.isAlive():
		print "peri_listener thread dead"
