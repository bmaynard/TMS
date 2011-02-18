from conf import settings

def authorized(auth_header):
	if settings.USERNAME == False:
		return True
	
	if not auth_header:
		return False

	auth_type, encoded_info = auth_header.split(None, 1)
	assert auth_type.lower() == 'basic'
	unencoded_info = encoded_info.decode('base64')
	username, password = unencoded_info.split(':', 1)
	return check_password(username, password)

def check_password(username, password):
	if (username == settings.USERNAME and password == settings.PASSWORD):
		return True
	return False