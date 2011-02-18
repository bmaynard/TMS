import threading
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from http.handler import Handler

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