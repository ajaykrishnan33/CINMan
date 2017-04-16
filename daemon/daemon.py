import thread
import requests
from background import get_system_info, maintain_contact
from auth_listen import auth_listener
# from usb_detect import usb_listener

# headers = {"Authorization" : "Token 3d7441c3bc2a224b1091c81ec7c152464aadc54c"}
# SERVER_URL = "http://localhost:8000/app/"

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

thread.start_new_thread(maintain_contact, (machine_id, headers, SERVER_URL))
thread.start_new_thread(auth_listener, (machine_id, headers, SERVER_URL))

while True:
	pass