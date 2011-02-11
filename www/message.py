from jinja2 import Environment, FileSystemLoader
from os.path import join, dirname, abspath

# Show the view for the message page

def process_request(request):
	ROOT = abspath(dirname(__file__))
	env = Environment(loader=FileSystemLoader(join(ROOT, 'templates')))
	template = env.get_template('message.html')
	
	message = {
				'mail_from': 'test',
				'mail_to': 'test',
				'content_type': 'test',
				'subject': 'test',
				'received_date': 'test',
				'message': 'test',
				'headers': 'test',
			}
	
	return template.render({'message' : message})
