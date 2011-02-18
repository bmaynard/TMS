import os
import sqlite3
from conf import settings

def connect():
	return sqlite3.connect(settings.DB_NAME, isolation_level=None)

def query(query, params=[]):
	conn = connect()
	cursor = conn.cursor()
	cursor.execute(query, params)
	conn.close()
	
def fetchall(query, params=[]):
	conn = connect()
	cursor = conn.cursor()
	cursor.execute(query, params)
	result_set = cursor.fetchall()
	conn.close()
	
	return result_set

def fetchone(query, params=[]):
	conn = connect()
	cursor = conn.cursor()
	cursor.execute (query, params)
	result = cursor.fetchone()
	conn.close()
	
	return result
	
def check_table_exists():
	conn = connect()
	cursor = conn.cursor()
	
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS `message` (
			`message_id` integer primary key,
			`mail_from` text,
			`mail_to` text,
			`content_type` text,
			`subject` text,
			`received_date` text,
			`text_body` text,
			`html_body` text,
			`original` text
			)
	''')
	
	conn.close()
	
def delete_db():
	if settings.DELETE_DB_ON_EXIT == True:
		os.remove(settings.DB_NAME)