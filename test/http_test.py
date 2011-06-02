import unittest
import sys
import base64
import urllib
from http.server import TMSWebServer
from httplib import HTTPConnection
from conf import settings
from db.query import check_table_exists, delete_db
from db.models.message import Message

class HttpTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):		
		cls.webServer = TMSWebServer(('0.0.0.0', 8080))
		cls.webServer.start()
		
	def setUp(self):
		# Create the db and a message
		check_table_exists()		
		Message().save(
						mail_from 	= 'testuser@from.com',
						mail_to		= 'testuser@to.com',
						subject		= 'unittest',
						text_body	= 'The Text Body',
						html_body	= 'The HTML Body',
						original	= 'Original Content'
						)
		
	def testIndex(self):
		# Test index page
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/")
		request = conn.getresponse()
		result = request.read()
		self.assertEqual(request.status, 200)
		self.assertGreater(result.find('testuser@from.com'), 0)
		
		# Delete a record, then test for no records
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/delete?id=1")
		request = conn.getresponse()
		request.read()
		
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/")
		request = conn.getresponse()
		result = request.read()
		self.assertEqual(request.status, 200)
		self.assertGreater(result.find('There are no emails stored in the database.'), 0)
		
		conn.close()
		
	def testImage(self):
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/images/blank.gif")
		request = conn.getresponse()
		request.read()
		self.assertEqual(request.status, 200)
		conn.close()
		
	def testMessage(self):		
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/message?id=1")
		request = conn.getresponse()
		result = request.read()
		self.assertEqual(request.status, 200)
		self.assertGreater(result.find('<div class="messagebox">'), 0)
		
		conn.request("GET", "/message?id=2")
		request = conn.getresponse()
		result = request.read()
		self.assertEqual(request.status, 200)
		self.assertGreater(result.find('Please select an email message from the list'), 0)
		
		conn.request("GET", "/message?id=-2")
		request = conn.getresponse()
		result = request.read()
		self.assertEqual(request.status, 200)
		self.assertGreater(result.find('Please select an email message from the list'), 0)
		
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/message?id=1&onlymsg=true")
		request = conn.getresponse()
		result = request.read()
		result.find('The HTML Body')
		self.assertEqual(request.status, 200)
		self.assertEqual(result, 'The HTML Body')
		
		conn.close()
	
	def testDelete(self):
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/delete?id=1")
		request = conn.getresponse()
		request.read()
		self.assertEqual(request.status, 301)
		
		conn.request("GET", "/delete?id=")
		request = conn.getresponse()
		result = request.read()
		self.assertGreater(result.find('Please select an email message from the list'), 0)
		
		conn.request("GET", "/delete?id=-1")
		request = conn.getresponse()
		result = request.read()
		self.assertGreater(result.find('Please select an email message from the list'), 0)
		
		conn.close()
	
	def testResponse404(self):
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/images/bad_file.gif")
		request = conn.getresponse()
		request.read()
		self.assertEqual(request.status, 404)
		conn.close()
		
	def testAuthentication(self):
		settings.USERNAME = 'test'
		settings.PASSWORD = 'test'
		
		# Test no password
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/")
		request = conn.getresponse()
		request.read()
		self.assertEqual(request.status, 401)
		
		# Test correct password
		base64string = base64.encodestring('%s:%s' % ('test', 'test'))[:-1]
		authheader =  "Basic %s" % base64string
		headers = {"Authorization": authheader}
		
		conn.request("GET", "/", urllib.urlencode({}), headers)
		request = conn.getresponse()
		request.read()
		self.assertEqual(request.status, 200)
		
		# Test incorrect password
		base64string = base64.encodestring('%s:%s' % ('test', 'bad_pass'))[:-1]
		authheader =  "Basic %s" % base64string
		headers = {"Authorization": authheader}
		
		conn.request("GET", "/", urllib.urlencode({}), headers)
		request = conn.getresponse()
		request.read()
		self.assertEqual(request.status, 401)
		
		conn.close()
				
		# Change the settings back for other tests
		settings.USERNAME = False
		settings.PASSWORD = False
		
	def tearDown(self):
		settings.DELETE_DB_ON_EXIT = True
		delete_db()
		
	@classmethod
	def tearDownClass(cls):
		cls.webServer.stop()

if __name__ == "__main__":
	unittest.main()