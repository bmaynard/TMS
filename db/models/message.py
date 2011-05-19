from db.model import Model, TextField, PrimaryKey

class Message(Model):
	def __init__(self):
		self.message_id = PrimaryKey()
		self.mail_from = TextField()
		self.mail_to = TextField()
		self.content_type = TextField(max_length=50)
		self.subject = TextField()
		self.received_date = TextField()
		self.text_body = TextField()
		self.html_body = TextField()
		self.original = TextField()