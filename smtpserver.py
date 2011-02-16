import sys
import asyncore
import threading
import smtpd
import MySQLdb
import email
import settings

# Catch any mail sent to the server and save it
class TMSSMTPServer(smtpd.SMTPServer):
	def __init__(self, localaddr, remoteaddr):
		smtpd.SMTPServer.__init__(self, localaddr, remoteaddr)
		
	def process_message(self, peer, mailfrom, rcpttos, data):
		try:
			try:
				msg = email.message_from_string(data)
				text_body = '';
				html_body = '';
				
				if msg.get_content_maintype() == 'multipart':
					for part in msg.get_payload():
						if part.get_content_type() == 'text/html':
							html_body = part.get_payload(decode=True)
							try:
								html_body = html_body.decode(part.get_content_charset())
								html_body = html_body.encode('utf-8') 
							except:
								print "Unable to decode/encode html email"
						else:
							if (text_body != ''):
								text_body += '%s' % '='*80
							text_body += part.get_payload(decode=True)
							try:
								text_body = text_body.decode(part.get_content_charset())
								text_body = text_body.encode('utf-8') 
							except:
								print "Unable to decode/encode text email"
							
				elif msg.get_content_maintype() == 'text':
					text_body = msg.get_payload(decode=True)
				
				db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASS, settings.MYSQL_DB)
				
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
						`text_body` = "''' + MySQLdb.escape_string(text_body) + '''",
						`html_body` = "''' + MySQLdb.escape_string(html_body) + '''",
						`headers` = "''' + MySQLdb.escape_string(data) + '''"		
				''')
				
				db.close()
				print '%s' % '='*80
				print 'New entry added to database'
			except Exception, e:
				print e
		except MySQLdb.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
			sys.exit(1)

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