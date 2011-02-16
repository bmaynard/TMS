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
		cursor.execute ("SELECT message_id, mail_from, mail_to, content_type, subject, received_date, text_body, html_body, headers FROM message WHERE message_id = %d" % message_id)
		result = cursor.fetchone()
		db.close()
	
		if request.parsed_query.has_key('onlymsg') == True:
			return result[7]
		
		# Due to UTF-8 and jinga, we will just print the text avoiding jinja template library
		# TODO: Fix this issue
		if request.parsed_query.has_key('onlytext') == True:
			return result[6]
		
		ROOT = abspath(dirname(__file__))
		env = Environment(autoescape=True,loader=FileSystemLoader(join(ROOT, 'templates')))
		template = env.get_template('message.html')
		
		has_text = False
		
		if result[6] != '':
			has_text = True
		
		message = {
					'message_id': result[0],
					'mail_from': result[1],
					'mail_to': result[2],
					'content_type': result[3],
					'subject': result[4],
					'received_date': result[5],
					'text_body': has_text,
					'html_body': result[7],
					'headers': result[8],
				}
		
		return template.render({'message' : message})
		
		return False		
	except Exception, e:
		print e
		ROOT = abspath(dirname(__file__))
		env = Environment(autoescape=True,loader=FileSystemLoader(join(ROOT, 'templates')))
		template = env.get_template('error.html')
		return template.render({'error_msg': 'Please select an email message from the list.'})