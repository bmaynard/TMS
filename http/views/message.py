from http.response import HttpRenderResponse
from db.models.message import Message
from db.model import ModelException

# Show the view for the message page

def process_request(request):
	try:
		message_id = int(request.parsed_query['id'][0])
		
		if message_id <= 0:
			raise Exception
		
		try:
			result = Message().get(message_id)
		except ModelException:
			raise Exception('Email message not found')
		
		if request.parsed_query.has_key('onlymsg') == True:
			return result['html_body']
		
		return HttpRenderResponse('message.html', {'message' : result})	
	except Exception:
		return HttpRenderResponse('error.html', {'error_msg': 'Please select an email message from the list.'})