import time
from conf import settings
from http.server import TMSWebServer
from smtp.server import TMSEmailServer
from db.query import check_table_exists, delete_db

if __name__ == "__main__":
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