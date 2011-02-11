# TMS (Temporary Mail Server)

TMS is a temporary mail server that you can run that will capture any mail server sent to the server, save it a MySQL database and provides a front end web client to view the email messages.

## Running TMS

TMS requires the following modules to be installed:

* Jinja2 (http://jinja.pocoo.org/)
* MySQLdb (http://mysql-python.sourceforge.net/MySQLdb.html)

Run the following command to start the TMS server. The port at the end is the SMTP port that the server will listen on.

	python tms.py 0.0.0.0:1082
	
You can visit the web client by going to:

	http://localhost:8181
	
## Note:

This project is still under active development and you will need to change the MySQL details in tms.py. I will be implementing a configuration file soon.