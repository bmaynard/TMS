# TMS (Temporary Mail Server)

TMS is a temporary mail server that you can run that will capture any mail server sent to the server, save it a sqlite3 database and provides a front end web client to view the email messages.

## Install TMS

TMS requires the following modules to be installed:

* Jinja2 (http://jinja.pocoo.org/)

First, rename settings.dist.py to settings.py and change any settings if needed.

## Running TMS

Run the following command to start the TMS server.

	python tms.py
	
You can visit the web client by going to:

	http://localhost:8181
	
Now set your email application to send email the the ip and port of the TMS server.