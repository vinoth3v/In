import json
import datetime

#-----------------------------------------------------------------------
#					ENTITY MODEL
#-----------------------------------------------------------------------



class EntityModelBase:
	'''Base entity Model class'''

@IN.register('Entity', type = 'Model')
class EntityModel(EntityModelBase):
	'''Base Entity Model

	Single entity can have multiple db tables to store its Data and field data
	'''

	# we will not update these db columns
	not_updatable_columns = ['id', 'type', 'created']
	json_columns = []

	
	#entity_type = 'Entity'

	set_deleted_status = False

	@property
	def model(self):
		'''return data model of this entity'''

		_model = IN.entitier.entity_model
		if self.entity_type in _model:
			return _model[self.entity_type]
		else:
			_model['default']

	def __init__(self, objcls, key, mem_type):

		self.entity_class = objcls
		self.entity_type = objcls.__type__

		#self.model = {} # will be set by entitier

	def load(self, id = None):
		'''Load entities of type

		type: type of the entity: nabar, content, profile

		id : int : load single entity
		id : None: load all entities
		id : any iterable: load multiple entities
		'''

		if id is None:
			return self.load_all()

		if type(id) is int:
			return self.load_single(id)

		# default is load multiple, id can be any iterable
		return self.load_multiple(id)

	def load_single(self, id):
		'''load single entity data from DB

		'''

		entity_data = {}

		if not id:
			return entity_data

		where = ['id', id]

		try:

			table_info = self.model['table']
			table = table_info['name']
			columns = table_info['columns']

			cursor = IN.db.select({
				'tables' : table,
				'where' : where,
			}).execute()

			if cursor.rowcount != 1:
				return None

			data = cursor.fetchone()

			for col in columns:
				try:
					entity_data[col] = data[col]
				except Exception as e:
					IN.logger.debug()
					pass

			return entity_data

		except Exception as er:
			IN.logger.debug()
			return None

	def load_multiple(self, ids):
		'''load multiple entities

		'''

		return self.load_all(ids)

	def load_all(self, ids = None):
		'''load all entities

		'''

		try:

			entities = {}

			table_info = self.model['table']
			table = table_info['name']
			columns = table_info['columns']

			json = {'tables' : table}

			if ids is not None:
				json['where'] = ['id', 'IN', ids]

			cursor = IN.db.select(json).execute()

			if cursor.rowcount == 0:
				return None

			for data in cursor:
				id = data['id']
				if id not in entities:
					entities[id] = {}

				entity_data = entities[id]

				for col in columns:
					try:
						entity_data[col] = data[col]
					except Exception as e:
						IN.logger.debug()
						pass

			# initiate the entity
			if not entities:
				return None

			return entities

		except Exception as er:
			IN.logger.debug()
			return None


	def select(self, where):
		'''select entity IDs by where conditions'''

		try:
			cursor = IN.db.select({
				'tables' : self.model['table']['name'],
				'columns' : ['id'],				# get id only
				'where' : where,
			}).execute()

			if cursor.rowcount == 0:
				return None

			# fetchall method will return list of 'tuples'
			return [data['id'] for data in cursor]

		except Exception as er:
			IN.logger.debug()
			return None

	def save(self, entity, commit = True):
		'''insert or update the entity'''
		if entity.id is None: # new entity
			return self.insert(entity, commit)
		return self.update(entity, commit)

	def insert(self, entity, commit = True):
		connection = IN.db.connection

		new_id = None

		try:
			#print(self.entity_class, self.entity_type, self.model)

			table_info = self.model['table']
			table = table_info['name']
			columns = table_info['columns']

			insert_values = {}

			for col in columns.keys():
				if col == 'id' and (not isinstance(entity.id, int) or entity.id <= 0): # id is serial primary key # ignore it on insert
					continue
				insert_values[col] = getattr(entity, col, None)

			# alter entity data
			self.insert_prepare(entity, insert_values)

			column_keys = []
			values = []

			for col, val in insert_values.items():
				column_keys.append(col)
				values.append(val)

			#print(values)
			cursor = IN.db.insert({
				'table' : table,
				'columns' : column_keys,
				'returning' : 'id',
			}).execute([values])

			new_id = cursor.fetchone()[0]

			#print('New entity id', new_id)

			fielder = IN.fielder
			for field_name, field in entity.items():
				
				# set the entity id
				field.entity_id = new_id
				field.entity_type = entity.__type__
				field.entity_bundle = entity.type
				field.entity = entity

				fielder.insert(field)

			# commit the changes
			if commit: # if not caller will handle the commit
				connection.commit()

			entity.id = new_id

			return new_id

		except Exception as e:
			if commit:
				connection.rollback()
			IN.logger.debug()
			raise e # re raise

	def update(self, entity, commit = True):
		# TODO:
		connection = IN.db.connection

		try:

			table_info = self.model['table']
			table = table_info['name']
			columns = table_info['columns']

			update_values = {}

			for col in columns.keys():
				if col == 'id' or col in self.not_updatable_columns:
					continue
				update_values[col] = getattr(entity, col, None)

			# alter entity data
			self.update_prepare(entity, update_values)

			column_keys = []
			values = []

			set = []
			for col, val in update_values.items():
				set.append([col, val])

			if set:
				cursor = IN.db.update({
					'table' : table,
					'set' : set,
					'where' : ['id', int(entity.id)]
				}).execute()

			# update fields
			fielder = IN.fielder

			for field_name, field in entity.items():
						
				# set the entity id
				field.entity_id = entity.id
				field.entity_type = entity.__type__
				field.entity_bundle = entity.type
				field.entity = entity

				fielder.update(field, False)

			if commit: # if not, caller will handle the commit
				connection.commit()

		except Exception as e:
			if commit:
				connection.rollback()
			IN.logger.debug()
			raise e # re raise

	def load_entity_additional_data(self, entity):
		'''load_entity_additional_data'''


	def delete(self, entity, commit = True):
		'''Delete a entity'''

		if isinstance(entity, Entity):
			id = entity.id
		else:
			id = int(entity)

		connection = IN.db.connection

		try:
			table = self.model['table']['name']

			if self.set_deleted_status:
				# set deleted flag instead of actual delete table row
				cursor = IN.db.update({
					'table' : table,
					'set' : [['status', IN.entitier.STATUS_DELETED]],
					'where' : ['id', int(entity.id)]
				}).execute()
			else:
				cursor = IN.db.delete({
					'table' : table,
					'where' : ['id', id]
				}).execute()

			# TODO: delete fields

			# commit the changes
			connection.commit()

		except Exception as e:
			connection.rollback()
			IN.logger.debug()
			raise e # re raise


	def table(self):
		try:
			return self.model['table']['name']
		except KeyError as e:
			return None

	def columns(self, table):
		try:
			return self.model['table']['columns'].keys()
		except KeyError as e:
			return None

	def fields(self, table):
		try:
			return self.model['fields'].keys()
		except KeyError as e:
			pass
		return {}


	def insert_prepare(self, entity, values):
		self.__prepare_json_columns__(entity, values)

	def update_prepare(self, entity, values):
		self.__prepare_json_columns__(entity, values)

	def __prepare_json_columns__(self, entity, values):

		for col in self.json_columns:
			if col in values:
				data = values[col]
				if type(data) is not str:
					try:
						values[col] = json.dumps(data, skipkeys = True, ensure_ascii = False)
					except Exception as e:
						IN.logger.debug()
						values[col] = '{}'
