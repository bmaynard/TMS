from db.model import Model, TextField, PrimaryKey

class Message(Model):
	message_id = PrimaryKey()
	mail_from = TextField()
	mail_to = TextField()
	content_type = TextField(max_length=50)
	subject = TextField()
	received_date = TextField()
	text_body = TextField()
	html_body = TextField()
	original = TextField()