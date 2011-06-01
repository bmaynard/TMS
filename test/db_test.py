import unittest

from db.model import ModelException
from db.models.message import Message
from db.query import check_table_exists, delete_db
from os import path
from conf import settings

class DBTest(unittest.TestCase):

	def testDB(self):
		check_table_exists()
		self.assertTrue(path.exists('temp.db'))
		
		Message().save(
						mail_from 	= 'testuser@from.com',
						mail_to		= 'testuser@to.com',
						subject		= 'unittest'
						)
		
		self.assertEquals(Message().get(1)['mail_from'], 'testuser@from.com')
		
		Message().save(
						mail_from 	= 'seconduser@from.com',
						mail_to		= 'seconduser@to.com',
						subject		= 'second unittest'
						)
		
		Message().save(
						message_id	= 1,
						mail_from 	= 'testuser@from.com',
						mail_to		= 'testuser@to.com',
						subject		= 'unittest'
						)
		
		
		self.assertEquals(len(Message().all()), 2)
		
		self.assertEquals(Message().order_by('message_id DESC').all()[0]['subject'], 'second unittest')
		
		Message().delete(1)
		self.assertRaises(ModelException, Message().get, 1)
		
		Message().delete(2)
		self.assertRaises(ModelException, Message().all)
	
		self.assertRaises(ModelException, Message().save, bad_key = True)
	
		settings.DELETE_DB_ON_EXIT = True
		delete_db()
		self.assertFalse(path.exists('temp.db'))
	def tearDown(self):
		if (path.exists('temp.db')):
			settings.DELETE_DB_ON_EXIT = True
			delete_db()

if __name__ == "__main__":
	unittest.main()