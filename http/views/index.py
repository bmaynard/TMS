from http.response import HttpRenderResponse
from db.query import fetchall
from db.models.message import Message

# Show the view for the index page

def process_request(request):
	try:
		result_set = Message().order_by('received_date DESC').all()
	except:
		result_set = False

	return HttpRenderResponse('index.html', {'rows': result_set})
