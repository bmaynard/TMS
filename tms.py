import time
import settings
from webserver import TMSWebServer
from smtpserver import TMSEmailServer
		
if __name__ == "__main__":
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
			print "TMS Stopped"