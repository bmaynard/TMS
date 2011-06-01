from urlparse import urlparse, parse_qs
import os
import mimetypes
from BaseHTTPServer import BaseHTTPRequestHandler
from http.views.route import urlroutes
from http.response import HttpResponseRedirect
from http.authentication import authorized

class AuthenticationException(Exception):
	pass

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			if authorized(self.headers.getheader('Authorization')) != True:
				raise AuthenticationException
			
			parsed_path = urlparse(self.path)
			
			if (urlroutes.has_key(parsed_path.path)):
				exec("import http.views." + urlroutes[parsed_path.path] + " as webmodule")
				parsed_path.parsed_query = parse_qs(parsed_path.query)
				response = webmodule.process_request(parsed_path)
				
				if isinstance(response, HttpResponseRedirect) == True:
					self.send_response(response.status_code)
					self.send_header('Location', response.url)
					self.end_headers()
				else:
					self.send_response(200)
					self.send_header("Content-type", "text/html; charset=UTF-8'")
					self.end_headers()
					self.wfile.write(response.encode('utf-8'))
			else:
				# Is the a file in the file system?
				ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), 'views/static'))
				
				try:
					file_path = ROOT + parsed_path.path
					f = open(file_path)
					
					self.send_response(200)
					mimetype, _ = mimetypes.guess_type(file_path)
					self.send_header('Content-type', mimetype)
					fs = os.fstat(f.fileno())
					self.send_header("Content-Length", str(fs[6]))
					self.end_headers()
					
					for s in f:
						self.wfile.write(s)
	
				except:
					self.send_response(404)
					self.send_header("Content-type", "text/html")
					self.end_headers()
					self.wfile.write("<html><title>Page Not Found</title><body><h1>Page Not Found!</h1>")
					self.wfile.write("</body></html>")
		except AuthenticationException:
			self.send_response(401)
			self.send_header('WWW-Authenticate', 'Basic realm="TMS Adminstration"')
			self.end_headers()
			self.wfile.write('<html><head><title>Authentication Required</title></head>');
			self.wfile.write('<body><h1>Authentication Required</h1>If you can\'t get in, then stay out.</body></html>')