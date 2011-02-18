from http.response import HttpRenderResponse, HttpResponseRedirect
from db.query import query

def process_request(request):
	try:
		message_id = int(request.parsed_query['id'][0])
		
		if message_id <= 0:
			raise Exception
		
		query("DELETE FROM message WHERE message_id = ?", [str(message_id)])
		
		return HttpResponseRedirect('/')
	except:
		return HttpRenderResponse('error.html', {'error_msg': 'Please select an email message from the list.'})