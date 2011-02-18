# TMS (Temporary Mail Server)

TMS is a temporary mail server that will capture any mail server sent to the server, save it a sqlite3 database and provides a front end web client to view the email messages.

## Install TMS

TMS requires the following module to be installed:

* Jinja2 (http://jinja.pocoo.org/)

If you need to change any settings eg: smtp or web port, set the username/password for the web client then you can edit the conf/settings.py file.

## Running TMS

Run the following command to start the TMS server.

	python tms.py

Now set your application to send email to the ip and port of the TMS server. You can visit the web client by going to:

	http://localhost:8181

## Notes

If you want to use basic http authentication to login into the web client, then change USERNAME and PASSWORD variables in conf/settings.py. Setting USERNAME to False will turn of the authentication mode.