from jinja2 import Environment, FileSystemLoader
from os.path import join, dirname, abspath
import MySQLdb
import settings

# Show the view for the message page

def process_request(request, Handler):
	ROOT = abspath(dirname(__file__))
	env = Environment(autoescape=True,loader=FileSystemLoader(join(ROOT, 'templates')))
	template = env.get_template('index.html')
	
	db = MySQLdb.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASS, settings.MYSQL_DB)
	
	cursor = db.cursor()
	cursor.execute ("SELECT message_id, mail_from, mail_to, subject, received_date FROM message ORDER BY received_date DESC")
	result_set = cursor.fetchall()
	
	
	db.close()
	return template.render({'rows': result_set})
