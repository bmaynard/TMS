from jinja2 import Environment, FileSystemLoader
from os.path import join, dirname, abspath

class HttpResponseRedirect():
	def __init__(self, url, status_code=301):
		self.url = url
		self.status_code = status_code
		
def HttpRenderResponse(filename, vars=None):
	ROOT = abspath(dirname(__file__))
	env = Environment(autoescape=True,loader=FileSystemLoader(join(ROOT, 'views/templates')))
	template = env.get_template(filename)
	
	return template.render(vars)