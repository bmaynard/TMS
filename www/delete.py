from jinja2 import Environment, FileSystemLoader
from os.path import join, dirname, abspath
import MySQLdb
import settings
# Show the view for the message page

def process_request(request, Handler):
	try:
		message_id = int(request.parsed_query['id'][0])
		
		if message_id <= 0:
			raise Exception
		
		db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASS, settings.MYSQL_DB)
	
		cursor = db.cursor()
		cursor.execute("DELETE FROM message WHERE message_id = %d" % message_id)
		db.close()
		
		Handler.send_response(301)
		Handler.send_header('Location', '/')
		Handler.end_headers()
		
		return False		
	except:
		ROOT = abspath(dirname(__file__))
		env = Environment(autoescape=True,loader=FileSystemLoader(join(ROOT, 'templates')))
		template = env.get_template('error.html')
		return template.render({'error_msg': 'Please select an email message from the list.'})