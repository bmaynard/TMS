import threading
from urlparse import urlparse, parse_qs
import os
import mimetypes
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import www.route
import settings

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if settings.USERNAME != False and self.authorized(self.headers.getheader('Authorization')) != True:
				raise Exception;
			
			parsed_path = urlparse(self.path)
			
			routes = www.route.urlroutes
			
			if (routes.has_key(parsed_path.path)):
				exec("import www." + routes[parsed_path.path] + " as webmodule")
				parsed_path.parsed_query = parse_qs(parsed_path.query)
				content = webmodule.process_request(parsed_path, self)
				
				if content != False:
					self.send_response(200)
					self.send_header("Content-type", "text/html; charset=UTF-8'")
					self.end_headers()
					self.wfile.write(content.encode('utf-8'))
				
			else:
				# Is the a file in the file system?
				ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'www/templates'))
				
				try:
					file_path = ROOT + parsed_path.path
					f = open(file_path)
					
					self.send_response(200)
					mimetype, _ = mimetypes.guess_type(file_path)
					self.send_header('Content-type', mimetype)
					self.end_headers()
					
					for s in f:
						self.wfile.write(s)
	
				except:
					self.send_response(404)
					self.send_header("Content-type", "text/html")
					self.end_headers()
					self.wfile.write("<html><title>Page Not Found</title><body><h1>Page Not Found!</h1>")
					self.wfile.write("</body></html>")
		except:
			self.send_response(401)
			self.send_header('WWW-Authenticate', 'Basic realm="TMS Adminstration"')
			self.end_headers()
			self.wfile.write('<html><head><title>Authentication Required</title></head>');
			self.wfile.write('<body><h1>Authentication Required</h1>If you can\'t get in, then stay out.</body></html>')
			
	def authorized(self, auth_header):
		if not auth_header:
			return False

		auth_type, encoded_info = auth_header.split(None, 1)
		assert auth_type.lower() == 'basic'
		unencoded_info = encoded_info.decode('base64')
		username, password = unencoded_info.split(':', 1)
		return self.check_password(username, password)

	def check_password(self, username, password):
		if (username == settings.USERNAME and password == settings.PASSWORD):
			return True
		return False

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
	pass

class TMSHTTPServer(ThreadingHTTPServer):
	def __init__(self, server_address, RequestHandlerClass):
		ThreadingHTTPServer.__init__(self, server_address, RequestHandlerClass)
		
class TMSWebServer(threading.Thread):
	def __init__(self, listen):
		threading.Thread.__init__(self)
		self._stopevent = threading.Event()
		self.server = TMSHTTPServer(listen, Handler)
		
	def run(self):
		self.server.serve_forever()
			
	def stop(self, timeout=None):
		self.server.server_close()
		self.server.shutdown()
		self._stopevent.set()
		threading.Thread.join(self, timeout)