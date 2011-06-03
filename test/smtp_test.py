import unittest
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtp.server import TMSEmailServer
from conf import settings
from db.query import check_table_exists, delete_db
from db.models.message import Message

class SmtpTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):		
		cls.mailServer = TMSEmailServer(('0.0.0.0', 8181))
		cls.mailServer.start()
		
	def setUp(self):
		check_table_exists()
		
	def testTextEmail(self):
		mailto = 'touser@test.com'
		mailfrom = 'fromuser@test.com'
		
		msg = MIMEText('This is a test email message')
		msg['Subject'] = 'Email Test'
		msg['From'] = mailto
		msg['To'] = mailfrom
		
		# Send the message via our test SMTP server
		s = smtplib.SMTP('localhost', 8181)
		s.sendmail(mailfrom, mailto, msg.as_string())
		s.quit()
		self.assertEquals(Message().get(1)['subject'], 'Email Test')
		
	def testHTMLEmail(self):
		mailto = 'touser@test.com'
		mailfrom = 'fromuser@test.com'
		
		msg = MIMEMultipart('alternative')
		msg['Subject'] = 'HTML/Text Email Test'
		msg['From'] = mailto
		msg['To'] = mailfrom
		
		text = 'This is the text body'
		html = "<html><body><p>This is the html body</p></body></html>"
		
		msg.attach(MIMEText(text, 'plain'))
		msg.attach(MIMEText(text, 'plain'))
		msg.attach(MIMEText(html, 'html'))
		
		# Send the message via our own SMTP server
		s = smtplib.SMTP('localhost', 8181)
		s.sendmail(mailfrom, mailto, msg.as_string())
		s.quit()
		result_text = text
		result_text += '%s' % '='*80
		result_text += text
		
		self.assertEquals(Message().get(1)['text_body'], result_text)
		self.assertEquals(Message().get(1)['html_body'], html)
	def tearDown(self):
		delete_db()
		
	@classmethod
	def tearDownClass(cls):
		cls.mailServer.stop()

if __name__ == "__main__":
	unittest.main()