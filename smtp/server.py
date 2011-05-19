import asyncore
import threading
import smtpd
import email
from db.models.message import Message
from datetime import datetime

# Catch any mail sent to the server and save it
class TMSSMTPServer(smtpd.SMTPServer):
	def __init__(self, localaddr, remoteaddr):
		smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
		
	def process_message(self, peer, mailfrom, rcpttos, data):
		try:
			msg = email.message_from_string(data)
			text_body = '';
			html_body = '';
			
			if msg.get_content_maintype() == 'multipart':
				for part in msg.get_payload():
					if part.get_content_type() == 'text/html':
						try:
							html_body = part.get_payload(decode=True)
							html_body = html_body.decode(part.get_content_charset())
						except:
							print "Unable to decode html email"
					else:
						if (text_body != ''):
							text_body += '%s' % '='*80
						try:
							text_body += part.get_payload(decode=True)
							text_body = text_body.decode(part.get_content_charset())
						except:
							print "Unable to decode text email"
						
			elif msg.get_content_maintype() == 'text':
				text_body = msg.get_payload(decode=True)
			
			Message().save(
						mail_from 	= msg['from'],
						mail_to		= msg['to'],
						content_type = msg.get_content_type(),
						subject		= msg['subject'],
						text_body	= text_body,
						html_body	= html_body,
						original	= data,
						received_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
						)
			
			print '%s' % '='*80
			print 'New email added to database (To: %s; Subject: %s) ' % (msg['to'], msg['subject'])
		except Exception, e:
			print e

class TMSEmailServer(threading.Thread):
	def __init__(self, listen):
		threading.Thread.__init__(self)
		self._stopevent = threading.Event()
		self.server = TMSSMTPServer(listen, None)
		
	def run(self):
		while not self._stopevent.isSet():
			asyncore.loop(timeout = 0.001, count = 1)
			
	def stop(self, timeout=None):
		self._stopevent.set()
		threading.Thread.join(self, timeout)
		self.server.close()