from http.response import HttpRenderResponse
from db.query import fetchone

# Show the view for the message page

def process_request(request):
	try:
		message_id = int(request.parsed_query['id'][0])
		
		if message_id <= 0:
			raise Exception
		
		result = fetchone("SELECT message_id, mail_from, mail_to, content_type, subject, received_date, text_body, html_body, original FROM message WHERE message_id = ?", [str(message_id)])
		
		if result == None:
			raise Exception('Email message not found')
	
		if request.parsed_query.has_key('onlymsg') == True:
			return result[7]
		
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
		
		return HttpRenderResponse('message.html', {'message' : message})
		
		return False		
	except:
		return HttpRenderResponse('error.html', {'error_msg': 'Please select an email message from the list.'})