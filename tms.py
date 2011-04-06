import time
import sys
from conf import settings
from http.server import TMSWebServer
from smtp.server import TMSEmailServer
from db.query import check_table_exists, delete_db
from db.models.message import Message
		
if __name__ == "__main__":
	print "starting"
	#test = Message.all()
	#print test
	test = Message.get(1)
	#print test
	print test.data['mail_from']
	test.save(mail_form="test@blah.com", mail_to="yeah@yeah.com")
	sys.exit()
	
	check_table_exists()
	
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
			delete_db()			
			print "TMS Stopped"