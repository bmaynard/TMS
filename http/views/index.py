from http.response import HttpRenderResponse
from db.query import fetchall

# Show the view for the index page

def process_request(request):	
	result_set = fetchall("SELECT message_id, mail_from, mail_to, subject, received_date FROM message ORDER BY message_id DESC")
	
	return HttpRenderResponse('index.html', {'rows': result_set})
