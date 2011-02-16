import time
import os
import settings
from webserver import TMSWebServer
from smtpserver import TMSEmailServer
import sqlite3
		
if __name__ == "__main__":	
	conn = sqlite3.connect('temp.db', isolation_level=None)
	cursor = conn.cursor()
	
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS `message` (
			`message_id` integer primary key,
			`mail_from` text,
			`mail_to` text,
			`content_type` text,
			`subject` text,
			`received_date` text,
			`text_body` text,
			`html_body` text,
			`original` text
			)
	''')
	
	conn.close()
	
	mailServer = TMSEmailServer((settings.LISTEN_IP, settings.SMTP_PORT))
	mailServer.start()
	
	webServer = TMSWebServer((settings.LISTEN_IP, settings.WEB_PORT))
	webServer.start()
	
	print "TMS Running"
	running = True
	
	while running == True:
		try:
			time.sleep(1)
		except:
			mailServer.stop()
			webServer.stop()
			del mailServer
			del webServer
			running = False
			
			if settings.DELETE_DB_ON_EXIT == True:
				os.remove('temp.db')
			
			print "TMS Stopped"