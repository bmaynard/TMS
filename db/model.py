from db import query

class ModelException(Exception):
	pass

class ClassProperty(property):
		def __get__(self, cls, owner):
				return self.fget.__get__(None, owner)()

class Model(object):
	data = None
	@classmethod
	def get(cls, id):
		result = query.fetchone("SELECT " + cls.build_fields() + " FROM " + str(cls.__name__).lower() + " WHERE " + cls.get_pk_field() + " = ?", [id])
		
		if result == None:
			raise ModelException("No results found")
		
		cls.data = {}
		
		for i in range(len(result)):
			if cls.__dict__.items()[i][0][:2] != '__':
				cls.data.update({cls.__dict__.items()[i][0]: result[i]})
		
		return cls
	
	@classmethod
	def all(cls):
		result = query.fetchall("SELECT " + cls.build_fields() + " FROM " + str(cls.__name__).lower())
		
		if result == None:
			raise ModelException("No results found")

		data = {}
		i = 0
		
		for row in result:
			row_data = {}
			for x in range(len(row)):
				row_data.update({cls.__dict__.items()[x][0]: row[x]})
			
			data.update({i: row_data})
			i = i + 1
			
		return data
	
	@classmethod
	def save(cls, **kwargs):
		if cls.data == None:
			query = "INSERT INTO "
		else:
			query = "UPDATE "
		print cls.data[cls.get_pk_field()]
		for key in kwargs:
			print "another keyword arg: %s: %s" % (key, kwargs[key])

		return True
	
	@classmethod
	def build_fields(cls):
		fields = ""
		
		for item in cls.__dict__.items():
			if isinstance(item[1], TextField) or isinstance(item[1], PrimaryKey):
				fields += item[0] + ","
			else:
				fields += "NULL," #TODO: We probally need to change this
			
		return fields[:-1]
	
	@classmethod
	def get_pk_field(cls):
		for item in cls.__dict__.items():
			if isinstance(item[1], PrimaryKey) == True:
				return item[0]
		
		raise ModelException("Unable to find PK")
	
class TextField():
	def __init__(self, max_length=False, blank=False):
		self.max_length = max_length
		self.blank = blank
	
	def __dict__(self):
		return self.__key__
		
class PrimaryKey():
	def __init__(self):
		self.blank = False