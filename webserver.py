import threading
from urlparse import urlparse, parse_qs
import os
import mimetypes
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import www.route

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
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