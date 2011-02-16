from jinja2 import Environment, FileSystemLoader
from os.path import join, dirname, abspath
import sqlite3

# Show the view for the message page

def process_request(request, Handler):
	ROOT = abspath(dirname(__file__))
	env = Environment(autoescape=True,loader=FileSystemLoader(join(ROOT, 'templates')))
	template = env.get_template('index.html')
	
	conn = sqlite3.connect('temp.db', isolation_level=None)
	
	cursor = conn.cursor()
	cursor.execute("SELECT message_id, mail_from, mail_to, subject, received_date FROM message ORDER BY message_id DESC")
	result_set = cursor.fetchall()
	conn.close()
	
	return template.render({'rows': result_set})
