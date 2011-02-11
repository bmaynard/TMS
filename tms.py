import sys
import asyncore
import threading
import smtpd
import time
import MySQLdb
import email
from webserver import TMSWebServer

# Catch any mail sent to the server and save it

class TMSSTMPServer(smtpd.SMTPServer):
	def __init__(self, localaddr, remoteaddr):
		smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
		
	def process_message(self, peer, mailfrom, rcpttos, data):
		try:
			try:
				msg = email.message_from_string(data)
				message_body = '';
				
				if msg.get_content_maintype() == 'multipart':
					for part in msg.get_payload():
						message_body += '%s' % '='*80
						message_body += part.get_pay_load()
				elif msg.get_content_maintype() == 'text':
					message_body = msg.get_payload()
	
				db = MySQLdb.connect("localhost", "vs", "vs", "tms")
				
				cursor = db.cursor()
				cursor.execute('''
					INSERT INTO
						`message`
					SET
						`mail_from` = "''' + MySQLdb.escape_string(msg['from']) + '''",
						`mail_to` = "''' + MySQLdb.escape_string(msg['to']) + '''",
						`content_type` = "''' + MySQLdb.escape_string(msg.get_content_type()) + '''",
						`subject` = "''' + MySQLdb.escape_string(msg['subject']) + '''",
						`received_date` = NOW(),
						`message` = "''' + MySQLdb.escape_string(message_body) + '''",
						`headers` = "''' + MySQLdb.escape_string(data) + '''"		
				''')
				print '%s' % '='*80
				print 'New entry added to database'
			except Exception, e:
				print e
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)
		
class TMSEmailServer(threading.Thread):
	def __init__(self, ipport):
		threading.Thread.__init__(self)
		self._stopevent = threading.Event()
		self.server = TMSSTMPServer(ipport, None)
		
	def run(self):
		while not self._stopevent.isSet():
			asyncore.loop(timeout = 0.001, count = 1)
			
	def stop(self, timeout=None):
		self._stopevent.set()
		threading.Thread.join(self, timeout)
		self.server.close()
		
if __name__ == "__main__":
	if len(sys.argv) != 2:
		print "Usage: ip:port"
		sys.exit(1)
		
	ar = sys.argv[1].split(":")
	ar[1] = int(ar[1])
	ipport = tuple(ar)
	mailServer = TMSEmailServer(ipport)
	mailServer.start()
	
	webServer = TMSWebServer(8181)
	webServer.start()
	
	print "TMS running"
	running = True
	
	while running == True:
		try:
			time.sleep(1)
		except:
			print "Stopping TMS"
			mailServer.stop()
			webServer.stop()
			del mailServer
			running = False