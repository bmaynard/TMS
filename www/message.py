from jinja2 import Environment, FileSystemLoader
from os.path import join, dirname, abspath
import sqlite3

# Show the view for the message page

def process_request(request, Handler):
	try:
		message_id = int(request.parsed_query['id'][0])
		
		if message_id <= 0:
			raise Exception
		
			
		conn = sqlite3.connect('temp.db', isolation_level=None)
		
		cursor = conn.cursor()
		cursor.execute ("SELECT message_id, mail_from, mail_to, content_type, subject, received_date, text_body, html_body, original FROM message WHERE message_id = ?", (str(message_id)))
		result = cursor.fetchone()
		conn.close()
	
		if request.parsed_query.has_key('onlymsg') == True:
			return result[7]
		
		ROOT = abspath(dirname(__file__))
		env = Environment(autoescape=True,loader=FileSystemLoader(join(ROOT, 'templates')))
		template = env.get_template('message.html')
		
		message = {
					'message_id': result[0],
					'mail_from': result[1],
					'mail_to': result[2],
					'content_type': result[3],
					'subject': result[4],
					'received_date': result[5],
					'text_body': result[6],
					'html_body': result[7],
					'original': result[8],
				}
		
		return template.render({'message' : message})
		
		return False		
	except Exception, e:
		print e
		ROOT = abspath(dirname(__file__))
		env = Environment(autoescape=True,loader=FileSystemLoader(join(ROOT, 'templates')))
		template = env.get_template('error.html')
		return template.render({'error_msg': 'Please select an email message from the list.'})