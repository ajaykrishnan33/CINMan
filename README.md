# CINMan

Server:
	sudo apt-get install python-pip

	In server/CINMan/ :
		pip install -r requirements.txt
		./runner.sh

	For shutting down the server:
		./killer.sh

Daemon:
	In daemon/ : 
		python install.py (only once, initially)
			Enter server IP:port config, username, password
		python daemon.py (subsequently)

Client:
	Open client/login.html in a browser