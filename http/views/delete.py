from http.response import HttpRenderResponse, HttpResponseRedirect
from db.models.message import Message

def process_request(request):
	try:
		message_id = int(request.parsed_query['id'][0])
		
		if message_id <= 0:
			raise Exception
		
		Message().delete(message_id)
		
		return HttpResponseRedirect('/')
	except:
		return HttpRenderResponse('error.html', {'error_msg': 'Please select an email message from the list.'})