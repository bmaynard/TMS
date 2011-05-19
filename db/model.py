from db import query

class ModelException(Exception):
	pass

class Model(object):
	order_by_sql = None
	
	'''
		Return the selected record for the current model
	'''
	def get(self, id):
		result = query.fetchone("SELECT " + self.build_fields() + " FROM " + str(self.__class__.__name__).lower() + " WHERE " + self.get_pk_field() + " = ?", [id])
		
		if result == None:
			raise ModelException("No results found")
		
		data = {}
		i = 0
		
		for item in self.__dict__.items():
			if isinstance(item[1], TextField) or isinstance(item[1], PrimaryKey):
				data.update({self.__dict__.items()[i][0]: result[i]})
				i = i + 1
		
		return data
	
	'''
		Delete the selected record
	'''
	def delete(self, id):
		query.query("DELETE FROM " + str(self.__class__.__name__).lower() + " WHERE " + self.get_pk_field() + " = ?", [id])
		return True
	
	'''
		Return all the results for the current model
	'''
	def all(self):
		sqlQuery = "SELECT " + self.build_fields() + " FROM " + str(self.__class__.__name__).lower()
		
		if self.order_by_sql != None:
			sqlQuery += " ORDER BY " + self.order_by_sql
		
		result = query.fetchall(sqlQuery)
		
		if result == None:
			raise ModelException("No results found")
		
		data = []
		
		# Build up a dictionary with the field name as the key 
		for row in result:
			row_data = {}
			i = 0
			for x in range(len(row)):
				if self.__dict__.items()[i][0] == 'order_by_sql': # Need a better way to deal with this
					i = i + 1
				row_data[self.__dict__.items()[i][0]] = row[x]
				i = i + 1
			data.append(row_data)
			
		#print row_data
		return data
	
	'''
		Set the order by field
	'''
	def order_by(self, order_by):
		self.order_by_sql = order_by
		
		return self
	
	'''
		Update/Insert a record in the current model
	'''
	def save(self, **kwargs):
		update = False
		
		if kwargs.get(self.get_pk_field(), False) == False:
			sqlQuery = "INSERT INTO " + str(self.__class__.__name__).lower() + " ("
		else:
			sqlQuery = "UPDATE " +  str(self.__class__.__name__).lower() + " SET "
			update = True
		
		values = ""
		params = []
		
		# Build up the values of the SQL Query
		for key in kwargs:
			if hasattr(self, key) == False:
				raise ModelException('Property: ' + key + ' does not exist')
			
			if key != self.get_pk_field():
				if update == False:
						sqlQuery += key + ","
						values += "?,"
				else:
					sqlQuery += "`" + key + "` = ?,"
					
				params.append(kwargs[key])
			
		# Join the query segments together
		if update == False:
			sqlQuery = sqlQuery[:-1] + ") VALUES (" + values[:-1] + ")"
		else:
			sqlQuery = sqlQuery[:-1] + " WHERE `" + self.get_pk_field() + "` = ?"
			params.append(kwargs[self.get_pk_field()])
		
		query.query(sqlQuery, params)
		return True
	
	'''
		Build up a list of fields for the current model
	'''
	def build_fields(self):
		fields = ""
		
		for item in self.__dict__.items():
			if isinstance(item[1], TextField) or isinstance(item[1], PrimaryKey):
				fields += item[0] + ","
		
		return fields[:-1]
	
	'''
		Return the name of the primary key for the current model
	'''
	def get_pk_field(self):
		for item in self.__dict__.items():
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