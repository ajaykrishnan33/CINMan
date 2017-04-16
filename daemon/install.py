import requests

username = raw_input("Enter username:")
password = raw_input("Enter password:")

SERVER_URL = "http://localhost:8000/app/"
LOGIN_URL = "http://localhost:8000/api-token-auth/"

r = requests.post(LOGIN_URL, data={"username":username, "password":password})
token = r.json()["token"]
f = open("config.txt", "w")
f.write(token+"\n"+SERVER_URL)
f.close()