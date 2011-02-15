# TMS (Temporary Mail Server)

TMS is a temporary mail server that you can run that will capture any mail server sent to the server, save it a MySQL database and provides a front end web client to view the email messages.

## Install TMS

TMS requires the following modules to be installed:

* Jinja2 (http://jinja.pocoo.org/)
* MySQLdb (http://mysql-python.sourceforge.net/MySQLdb.html)

First, rename settings.dist.py to settings.py and insert your MySQL details and change any ports if needed.

Run the following sql:

	CREATE TABLE IF NOT EXISTS `message` (
	  `message_id` int(11) NOT NULL AUTO_INCREMENT,
	  `mail_from` text CHARACTER SET latin1 NOT NULL,
	  `mail_to` text CHARACTER SET latin1 NOT NULL,
	  `content_type` varchar(255) CHARACTER SET latin1 NOT NULL,
	  `subject` varchar(255) CHARACTER SET latin1 NOT NULL,
	  `received_date` datetime NOT NULL,
	  `text_body` text CHARACTER SET latin1 NOT NULL,
	  `html_body` text CHARACTER SET latin1 NOT NULL,
	  `headers` text CHARACTER SET latin1 NOT NULL,
	  PRIMARY KEY (`message_id`)
	) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

## Running TMS

Run the following command to start the TMS server.

	python tms.py
	
You can visit the web client by going to:

	http://localhost:8181
	
Now set your email application to send email the the ip and port of the TMS server.