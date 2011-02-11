import threading
import urlparse
import os
import mimetypes
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import www.route

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		parsed_path = urlparse.urlparse(self.path)
		
		routes = www.route.url_routes()
		
		if (routes.has_key(parsed_path.path)):
			exec("import www." + routes[parsed_path.path] + " as webmodule")
			content = webmodule.process_request(parsed_path)
			
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			self.wfile.write("%s" % content)
			
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
	def __init__(self, port):
		threading.Thread.__init__(self)
		self._stopevent = threading.Event()
		self.server = TMSHTTPServer(('', port), Handler)
		
	def run(self):
		self.server.serve_forever()
			
	def stop(self, timeout=None):
		self.server.server_close()
		self.server.shutdown()
		self._stopevent.set()
		threading.Thread.join(self, timeout)

'''
class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write("Hello World!")

class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
	pass

class serve_on_port(Thread):
	def __init__(self, port):
		self.server = ThreadingHTTPServer(('',port), Handler)
		self.server.serve_forever()

	def run(self):
		while not self._stopevent.isSet():
			asyncore.loop(timeout = 0.001, count = 1)

	def stop(self, timeout=None):
		self._stopevent.set()
		Thread.join(self, timeout)
		self.server.server_close()

class TMSWebServer():		
	def start(self):
		port = 8181
		
		self.httpdThread = Thread(target=serve_on_port, args=[port])
		self.httpdThread.start()
		print "WebServer Up"
		
	def stop(self):
		self.httpdThread.__stop()


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
	pass

def serve_on_port(port):
	server = ThreadingHTTPServer(('',port), Handler)
	server.serve_forever()
	print "Web Server Started"

class TMSWebServer():		
	def start(self):
		httpd = False
		return httpd
		
		
		self.httpdThread = Thread(target=serve_on_port, args=[port])
		self.httpdThread.start()
		print "WebServer Up"
		
	def stop(self):
		self.httpdThread.__stop()'''
	
'''
class TMSWebServer(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._stopevent = threading.Event()
		self.server = self.startServer()
		
	def run(self):
		while not self._stopevent.isSet():
			asyncore.loop(timeout = 0.001, count = 1)
			
	def stop(self, timeout=None):
		self._stopevent.set()
		threading.Thread.join(self, timeout)
		self.server.close()
		
	def startServer(self):
		port = 8181
		
		handler = SimpleHTTPServer.SimpleHTTPRequestHandler
		httpd = BaseHTTPServer.HTTPServer(('', port), handler)
		
		try:
			httpd.serve_forever()
		except KeyboardInterrupt:
			print 'Server killed on user request (keyboard interrupt).'
'''