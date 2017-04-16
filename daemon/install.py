import requests

server_ip = raw_input("Enter server ip:")
username = raw_input("Enter username:")
password = raw_input("Enter password:")

SERVER_URL = "http://" + server_ip + "/app/"
LOGIN_URL = "http://" + server_ip + "/api-token-auth/"

r = requests.post(LOGIN_URL, data={"username":username, "password":password})
token = r.json()["token"]
f = open("config.txt", "w")
f.write(token+"\n"+SERVER_URL)
f.close()