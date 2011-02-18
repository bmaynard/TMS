# TMS (Temporary Mail Server)

TMS is a temporary mail server that will capture any mail server sent to the server, save it a sqlite3 database and provides a front end web client to view the email messages.

## Install TMS

TMS requires the following module to be installed:

* Jinja2 (http://jinja.pocoo.org/)

You will need to rename settings.dist.py to settings.py and change any settings if needed.

## Running TMS

Run the following command to start the TMS server.

	python tms.py

Now set your application to send email to the ip and port of the TMS server. You can visit the web client by going to:

	http://localhost:8181

## Notes

If you want to use basic http authentication to login into the web client, then change USERNAME and PASSWORD variables in settings.py. Setting USERNAME to False will turn of the authentication.