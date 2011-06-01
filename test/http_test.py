import unittest
import sys

from http.server import TMSWebServer
from httplib import HTTPConnection

class HttpTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.webServer = TMSWebServer(('0.0.0.0', 8080))
		cls.webServer.start()
		
	def testResponse200(self):
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/")
		request = conn.getresponse()
		request.read()
		self.assertEqual(request.status, 200)
		conn.request("GET", "/images/blank.gif")
		request = conn.getresponse()
		request.read()
		self.assertEqual(request.status, 200)
		conn.close()
	
	def testResponse404(self):
		conn = HTTPConnection('localhost:8080')
		conn.request("GET", "/images/bad_file.gif")
		request = conn.getresponse()
		request.read()
		self.assertEqual(request.status, 404)
		conn.close()
		
	@classmethod
	def tearDownClass(cls):
		cls.webServer.stop()
		

if __name__ == "__main__":
	unittest.main()