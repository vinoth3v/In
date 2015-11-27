import json
import datetime


class FielderEngine:
	'''Field controller

	Fielder

	Field Type: int, date, text, textarea, select, options, image, ...
		Model : no real table. just general table structure, columns

	Field instance 	: instance of Field Types. attached to entity bundle
					: profile : name field instance of type 'text'
					: Customer : image field instance of type 'image'
					: node	 : tages field instance of type 'tag'

		Model : actual table with table structure of field types

	'''

	#fielders = Fielders()

	def __init__(self):

		self.field_model = RDict() # {}		# supports deep merge
		self.entity_field_config = RDict() # {}

		# field names are unique/table
		self.field_instance_config = RDict() #{}

		# all field types
		self.field_types = {}
		for field in IN.register.get_sub_classes_yield(Field):
			self.field_types[field.__type__] = field
		
		
		self.build_entity_field_config()
		
		# cache field table prefixes
		self.table_prefix = {}
		
	def build_entity_field_config(self):
		'''build the field config'''

		entity_field_config = IN.hook_invoke('entity_field_config')
		for config in entity_field_config:
			self.entity_field_config.update(config)

		# lets other addons to alter
		IN.hook_invoke('entity_field_config_alter', self.entity_field_config)

		# field_instance_config
		# config per field name
		for entity_type, bundle in self.entity_field_config.items():
			for bundle_name, fields in bundle.items():
				for field_name, field_config in fields.items():
					self.field_instance_config[field_name] = field_config


		# field model
		field_model = IN.hook_invoke('field_model')
		for model in field_model:
			self.field_model.update(model)

		# alter
		IN.hook_invoke('entity_field_model_alter', self.field_model)

		# update

		#for field_type, field_class in self.field_types.items():
			#if field_type in self.field_model:
				#field_class.Model.model = self.field_model[field_type].copy()
			#else:
				## use default model
				#field_class.Model.model = self.field_model.get('default', {}).copy()
				
			
			#field_class.Model.model['table_prefix'] = {} # lazy, 
		
	def bundle_fields(self, entity_type, bundle):
		try:
			return self.entity_field_config[entity_type][bundle]
		except Exception as e:
			return {}
		
	def field_config(self, entity_type, entity_bundle, field_name):
		try:
			return self.entity_field_config[entity_type][entity_bundle][field_name]
		except KeyError as e:
			return {}
			
	def field_table(self, field_name):
		'''returns prefixed table name for this field name

		prefix is depends on field_name'''
		
		try:
			return self.table_prefix[field_name]
		except KeyError:
			prefixes = IN.db.__conn__.db_settings['table_prefix']

			prefix = prefixes.get(field_name, None) or prefixes.get('field', None) or prefixes.get('default', '')
			prefix = prefix + field_name
			
			self.table_prefix[field_name] = prefix
			
		return prefix

	def load(self, entity_type, field_type, entity_ids, field_name):
		'''Load values of field instance that is attached to a bundle

		'''

		return self.field_types[field_type].Fielder.load(entity_type, entity_ids, field_name)

	#def select(self, type, where):
		#'''load fields by where conditions'''

		#return self.field_types[type].Fielder.select(where)

	def save(self, field, commit = True):
		return field.Fielder.save(field, commit)

	def insert(self, field, commit = True):
		return field.Fielder.insert(field, commit)

	def update(self, field, commit = True):
		return field.Fielder.update(field, commit)

	def delete(self, field, commit = True):
		return field.Fielder.delete(field, commit)

	def form_field(self, field_type, field_config, field_value = None):
		'''returns form field based on field type field data'''
		
		return self.field_types[field_type].Fielder.form_field(field_config, field_value)
		
	def __create_new_field__(self, entity_type, entity_bundle, field_type, field_name, status, weight, data):
		'''Create a new field to entity and create field db table'''

		connection = IN.db.connection
		
		try:

			table = 'config.config_entity_field'

			columns = [
				'entity_type', 'entity_bundle',
				'field_type', 'field_name',
				'weight', 'data', 'status'
			]

			data = json.dumps(data, skipkeys = True, ensure_ascii = False)

			values = [
				entity_type, entity_bundle,
				field_type, field_name,
				weight, data, status
			]
			cursor = IN.db.insert({
				'table' : table,
				'columns' : columns,
			}).execute([values])

			# creates table in DB for this field if table not already exists
			self.field_types[field_type].Model.__create_field_table__(field_name)
			
			# commit the changes
			connection.commit()
			
			# clear field cache
			self.entity_field_config = {}
			self.build_entity_field_config()
			
			return True

		except Exception as e:
			connection.rollback()
			IN.logger.debug()
			raise e # re raise

	def formatter_class(self, type):
		cls = IN.register.get_class(type, 'FieldFormatter')
		if cls is None:
			cls = In.field.field_formatter.FieldFormatter # use the default
		return cls
		
	#def field_formatter(self, entity_type, entity_bundle, view_mode, field_name):
		#'''returns the field formatter object'''
		## TODO: cache it
		#field_config = self.field_config(field_name)
		#field_type = field_config['field_type']
		
		#try:
			#return self.entity_field_config[entity_type][entity_bundle][field_name]['display_config'][view_mode]['field_formatter']
		#except KeyError as e:
			#return {}
		
		
	def field_display_config(self, entity_type, entity_bundle, view_mode, field_name):
		'''returns the config for entity_type, entity_bundle, view_mode, field_name'''
		
		try:
			return self.entity_field_config[entity_type][entity_bundle][field_name]['data']['display_config'][view_mode]
		except KeyError as e:
			# use default config
			if view_mode != 'default':
				try:
					return self.entity_field_config[entity_type][entity_bundle][field_name]['data']['display_config']['default']
				except KeyError as e:
					pass
			return {}
		
	def set_field_formatter_config(self, entity_type, entity_bundle, view_mode, field_name, config):
		'''save the field formatter config'''
		
		# get config from DB
		
		table = 'config.config_entity_field'
		
		where = [
			['entity_type', entity_type], 
			['entity_bundle', entity_bundle],
			['field_name', field_name],
		]
		
		try:
		
			cursor = IN.db.select({
				'tables' : table,
				'columns' : ['data'],
				'where' : where,
			}).execute()
			
		except Exception as e:
			raise e
		
		if cursor.rowcount != 1:
			raise In.field.FieldExceptionInvalidField(s('Invalid field {field_name}', {'field_name' : field_name}))

		data = cursor.fetchone()[0]
		
		# update
		
		if 'display_config' not in data:
			data['display_config'] = {}
		
		if view_mode not in data['display_config']:
			data['display_config'][view_mode] = {}
		
		data['display_config'][view_mode].update(config)
		
		# save config to DB
		
		data = json.dumps(data, skipkeys = True, ensure_ascii = False)
		
		set = [['data', data]]
		
		connection = IN.db.connection
		
		try:
			
			cursor = IN.db.update({
				'table' : table,
				'set' : set,
				'where' : where,
			}).execute()
			
			connection.commit()
			
		except Exception as e:
			connection.rollback()
			raise e
			
	def set_field_config_data(self, entity_type, entity_bundle, field_name, data):
		'''save the field formatter config'''
		
		# get config from DB
		
		table = 'config.config_entity_field'
		
		where = [
			['entity_type', entity_type], 
			['entity_bundle', entity_bundle],
			['field_name', field_name],
		]
		
		try:
		
			cursor = IN.db.select({
				'tables' : table,
				'columns' : ['data'],
				'where' : where,
			}).execute()
			
		except Exception as e:
			raise e
		
		if cursor.rowcount == 0:
			db_data = {}
		else:
			db_data = cursor.fetchone()[0]
		
		# update
		
		db_data.update(data)
		
		data = db_data
		
		# save config to DB
		
		data = json.dumps(data, skipkeys = True, ensure_ascii = False)
		
		set = [['data', data]]
		
		connection = IN.db.connection
		
		try:
			
			cursor = IN.db.update({
				'table' : table,
				'set' : set,
				'where' : where,
			}).execute()
			
			connection.commit()
			
		except Exception as e:
			connection.rollback()
			raise e
		
	def supported_field_formatters(self, field_type):
		
		formatters = {}
		
		try:
			types = IN.register.registered_classes_sorted[field_type]['FieldFormatter']
			if not types:
				types = []
		except Exception as e:
			IN.logger.debug()
			
		for cls in types:
			formatters[cls.__name__] = cls.__info__
		
		# TODO: get formatters from base Field types
		
		# get the class type
		field_class = IN.register.get_class(field_type, 'Field')
		if field_class:
			bases = field_class.__bases__
		
			for base in bases:
				base_formatters = self.supported_field_formatters(base.__type__)
				if base_formatters:
					formatters.update(base_formatters)
		
		return formatters
	
	def get_enity_bundle_field_config_from_db(self, entity_type, entity_bundle, field_name = None):
		'''always get fresh config from db'''
		
		config = {}

		try:
			
			where = [
				['entity_type', entity_type],
				['entity_bundle', entity_bundle],
			]
			if field_name is not None:
				where.append(['field_name', field_name])
				
			cursor = IN.db.select({
				'table' : 'config.config_entity_field',
				'where' : where
			}).execute()
			
			if cursor.rowcount == 0:
				return {}

			for row in cursor:
				field_type = row['field_type']
				field_name = row['field_name']
				weight = row['weight']
				data = row['data']

				config[field_name] = {
					'field_type' : field_type,
					'field_name' : field_name,
					'weight' : weight,
					'data' : data,
				}

		except Exception as e:
			IN.logger.debug()

		return config

#********************************************************************
#					Field 
#********************************************************************	



class FieldMeta(ObjectMeta):

	__class_type_base_name__ = 'FieldBase'
	__class_type_name__ = 'Field'

class FieldBase(Object, metaclass = FieldMeta):
	'''Base class of all IN Field.

	'''
	__allowed_children__ = None
	__default_child__ = None
	

@IN.register('Field', type = 'Field')
class Field(FieldBase):
	'''Base Field class.

	'''
	
	# Field id == name == field_name 
	@property
	def field_name(self):
		return self.id
	
	@field_name.setter
	def field_name(self, name):
		self.id = name
		
	def __init__(self, data = None, items = None, **args):

		self.language = ''
		self.entity_type = ''
		self.entity_bundle = ''
		
		if data is None:
			data = {}
		
		
		super().__init__(data, items, **args)


	@staticmethod
	def new(type, *pargs, **kargs):
		'''Overrides Object.new to get object of type Field.'''

		# get the class type
		objclass = IN.register.get_class(type, 'Field')
		if objclass is None:
			objclass = Field
			
		obj = objclass(*pargs, **kargs)

		return obj

	# easy methods
	def save(self, commit = True):
		return self.Fielder.save(self, commit)

	def insert(self, commit = True):
		return self.Fielder.insert(self, commit)

	def update(self, commit = True):
		return self.Fielder.update(self, commit)

	def delete(self, commit = True):
		return self.Fielder.delete(self, commit)



#********************************************************************
#					Field Fielder
#********************************************************************	


class FieldFielderBase:
	'''Base field Fielder class'''

@IN.register('Field', type = 'Fielder')
class FieldFielder(FieldFielderBase):
	'''Base Field Fielder'''

	
	#field_type = 'Field'

	def __init__(self, objcls, key, mem_type):
		self.field_class = objcls
		self.field_type = objcls.__type__

		# cacher is not available here
		#self.cacher = IN.cacher.cachers['field_' + self.field_type]
		self.__cacher__ = None

	#def field_config(self, field):
		#'''returns the field config from fielder'''
		#fielder = IN.fielder
		#try:
			#return fielder.entity_field_config[field.entity_type][field.entity_bundle][field.name]
		#except:
			#return { # default
				#'title' : '',
				#'weight' : 0,
				#'language' : '',
			#}
		
			
	@property
	def cacher(self):
		if self.__cacher__ is None:
			self.__cacher__ = IN.cacher.cachers['field_' + self.field_type]
		return self.__cacher__

	def load(self, entity_type, entity_ids, field_name):
		'''Load fields values

		'''
		
		if type(entity_ids) is int:
			result = self.load_single(entity_type, entity_ids, field_name)
			
			return result

		# default is load multiple, id can be any iterable
		result = self.load_multiple(entity_type, entity_ids, field_name)
		
		return result

	def load_single(self, entity_type, entity_id, field_name):
		'''load single field values

		'''

		# TODO: use the cache

		# load from DB
		field_data = self.field_class.Model.load_single(entity_type, entity_id, field_name)

		if not field_data:
			return None

		# initiate the field
		data = {
			'value' : field_data,
			'id' : field_name,
			'name' : field_name,
			'entity_type' : entity_type,
			'entity_id' : entity_id
		}
		
		field = self.field_class(data)

		return field

	def load_multiple(self, entity_type, entity_ids, field_name):
		'''load multiple fields

		'''

		# TODO: use the cache?

		entity_field_data = self.field_class.Model.load_multiple(entity_type, entity_ids, field_name)
		
		if not entity_field_data:
			return None
		
		# initiate the field
		for id, field_data in entity_field_data.items():
			# pass instance attributes
			data = {
				'value' : field_data,
				'id' : field_name,
				'name' : field_name,
				'entity_type' : entity_type,
				'entity_id' : id
			}
			
			field = self.field_class(data)
			entity_field_data[id] = field
			
		
		return entity_field_data


	#def select(self, where):
		#'''load fields by where conditions'''

		## model.select only returns ids
		#ids = self.field_class.Model.select(where)

		#if ids is None:
			#return None

		#return self.load_multiple(ids)


	def save(self, field, commit = True):
		return field.Model.save(field, commit)

	def insert(self, field, commit = True):
		# cache will be set on next load
		self.prepare_insert(field)
		return field.Model.insert(field, commit)

	def update(self, field, commit = True):
		# TODO: clear the cache
		self.prepare_update(field)
		return field.Model.update(field, commit)

	def delete(self, field, commit = True):
		# TODO: clear the cache
		return field.Model.delete(field, commit)

	def form_field(self, field_config, field_value = None):
		'''returns form field based on field type field data'''
		# not implemented error
		return None

	def prepare_insert(self, field):
		'''prepare the field submit values to insert'''
		pass

	def prepare_update(self, field):
		'''prepare the field submit values to update'''
		pass
	

#********************************************************************
#					Field Model
#********************************************************************	



class FieldModelBase:
	'''Base field Model class'''

@IN.register('Field', type = 'Model')
class FieldModel(FieldModelBase):
	'''Base Field Model

	Single field can have multiple db tables to store its Data and field data

	Entity
		field_interests : {
			'' : [							# default language
				{value : 'value0'},
				{value : 'value1'},
				{value : 'value2'},
			]
		}

	'''

	
	#field_type = 'Field'
	
	field_model_cache = None
	
	@property
	def model(self):
		
		if self.field_model_cache is not None:
			# use cached version
			return self.field_model_cache
		
		field_model = IN.fielder.field_model
		
		# use copied version, model may change based on field name
		if self.field_type in field_model:
			self.field_model_cache = field_model[self.field_type].copy()
		else:
			self.field_model_cache = field_model['default'].copy()
		
		return self.field_model_cache
		
		
	def __init__(self, objcls, key, mem_type):
		self.field_class = objcls
		self.field_type = objcls.__type__
		
		# changed as property
		#self.model = {} # will be set by fielder

	def load(self, entity_type, entity_ids):
		'''Load fields of type

		'''
		if type(entity_ids) is int:
			return self.load_single(entity_type, entity_ids)

		# default is load multiple, id can be any iterable
		return self.load_multiple(entity_type, entity_ids)

	def load_single(self, entity_type, entity_id, field_name):
		'''load single field

		'''

		try:

			table = IN.fielder.field_table(field_name)
			columns = self.model['columns'].copy() # we modify
			where = [['entity_type', entity_type], ['entity_id', entity_id]]

			# we dont need to load column that we already know
			del columns['entity_type']
			del columns['entity_id']

			columns = list(columns.keys())

			cursor = IN.db.select({
				'tables' : table,
				'columns': columns,
				'where' : where,
				'order' : ['weight'],
			}).execute()

			if cursor.rowcount <= 0:
				return None

			field_data = {}

			for data in cursor:
				values = {}
				language = ''
				weight = 0

				for col in columns:
					value = data[col]
					if col == 'language':
						if value is None:
							value = ''
						language = value
						continue
					if col == 'weight':
						weight = value
						continue
						
					values[col] = value

				if not values:
					continue

				if language not in field_data:
					field_data[language] = {}

				field_data[language][weight] = values

			return field_data

		except Exception as er:
			IN.logger.debug()
			return None

	def load_multiple(self, entity_type, entity_ids, field_name):
		'''load multiple fields

		'''

		entities = {}

		try:

			table = IN.fielder.field_table(field_name)
			
			columns = self.model['columns'].copy() # we modify
			where = [
				['entity_type', entity_type],
				['entity_id', 'IN', entity_ids]
			]

			# we dont need to load column that we already know
			del columns['entity_type']

			columns = list(columns.keys())

			cursor = IN.db.select({
				'tables' : table,
				'columns': columns,
				'where' : where,
				'order' : ['weight'],
			}).execute()

			if cursor.rowcount <= 0:
				return None

			for data in cursor:
				values = {}
				language = ''
				entity_id = 0
				weight = 0
				for col in columns:
					value = data[col]
					if col == 'entity_id':
						entity_id = value
						continue
					if col == 'language':
						if value is None:
							value = ''
						language = value
						continue
					if col == 'weight':
						weight = value
						continue
					values[col] = value

				if int(entity_id) == 0 or not values:
					# unknown error?
					continue

				if entity_id not in entities:
					entities[entity_id] = {}

				entity_field_data = entities[entity_id]

				if language not in entity_field_data:
					entity_field_data[language] = {}

				entity_field_data[language][weight] = values
				
			return entities

		except Exception as er:
			IN.logger.debug()
			return None

	def save(self, field, commit = True):
		'''insert or update the field'''
		if field.id is None: # new field
			return self.insert(field, commit)
		return update(field, commit)

	def insert(self, field, commit = True):
		connection = IN.db.connection

		try:

			entity_type = field.entity_type
			entity_id = field.entity_id
			created = datetime.datetime.now()
			
			field_values = field.value
			if not field_values: # None or {}
				return

			table = IN.fielder.field_table(field.field_name)
			
			columns = self.model['columns']

			column_keys = []
			
			for col in columns.keys():
				if col != 'id': # id is serial primary key # ignore it on insert
					column_keys.append(col)
			
			new_idx = 0
			qvalues = []
			for lang, lang_value in field_values.items():				
				for idx, field_value in lang_value.items():					
					
					rvalues = []
					
					for col in column_keys:
						if col == 'weight':
							# use new idx that starts from 0
							rvalues.append(int(new_idx))
							new_idx += 1
							continue
						if col == 'language':
							rvalues.append(lang)
							continue
							
						if col == 'entity_type':
							rvalues.append(entity_type)
							continue
						if col == 'entity_id':
							rvalues.append(entity_id)
							continue
						if col == 'created':
							rvalues.append(created)
							continue
							
						rvalues.append(field_value.get(col, None))
					
					qvalues.append(rvalues)
			
			cursor = IN.db.insert({
				'table' : table,
				'columns' : column_keys,
			}).execute(qvalues)


			# commit the changes
			if commit: # caller will handle the commit
				connection.commit()

			return True

		except Exception as e:
			if commit:
				connection.rollback()
			IN.logger.debug()
			raise e # re raise

	def update(self, field, commit = True):
		
		# delete first
		self.delete(field, commit)

		# and insert
		self.insert(field, commit)

		return True

	def delete(self, field, commit = True):
		'''Delete a field'''

		connection = IN.db.connection

		try:
			
			table = IN.fielder.field_table(field.field_name)
			entity_type = field.entity_type
			entity_id = field.entity_id
			
			cursor = IN.db.delete({
				'table' : table,
				'where' : [
					['entity_type', entity_type],
					['entity_id', entity_id],
				]
			}).execute()


			# commit the changes
			if commit:
				connection.commit()

		except Exception as e:
			if commit:
				connection.rollback()
			IN.logger.debug()
			raise e # re raise

	def __create_field_table__(self, field_name):

		'''Creates table in DB for this field'''
		field_type = self.field_type
		table = IN.fielder.field_table(field_name)
		q = ['CREATE TABLE IF NOT EXISTS ']
		q.append(table)
		q.append(''' (
			id bigserial PRIMARY KEY,
			entity_type character varying(64),
			entity_id bigint,
			language character varying(5),
			weight smallint,
			value text,
			created timestamp without time zone,
			status smallint DEFAULT 1			
		);''')

		## index
		#q.append('CREATE INDEX ')

		#index_name = table.split('.')[-1]

		#q.append(index_name + '_idx ')
		
		#q.append(' ON ' + table)
		#q.append(' USING btree ')
		#q.append(''' (
			#entity_type,
			#entity_id,
			#weight
		#);''')

		IN.db.execute(''.join(q))

		# caller will commit
		
#@IN.hook
#def __In_app_init__(app):
	## set the Field

	#IN.fielder = FielderEngine()


#********************************************************************
#					Field Themer
#********************************************************************	


@IN.register('FieldBase', type = 'Themer')
class FieldBaseThemer(In.themer.ObjectThemer):
	'''base field themer'''
		
@IN.register('Field', type = 'Themer')
class FieldThemer(FieldBaseThemer):
	
	@classmethod
	def field_formatter(cls, field, format, view_mode, args):
		'''returns field formatter for field type'''
		
		display_config = IN.fielder.field_display_config(field.entity_type, field.entity_bundle, view_mode, field.field_name)
		
		formatter = display_config.get('field_formatter', 'FieldFormatter')
		formatter_class = IN.fielder.formatter_class(formatter)
		
		# TODO: cache it
		
		return In.field.FieldFormatter()
		
	def theme(self, field, format, view_mode, args):
		theme_output = field.theme_current_output
		
		#formatter = self.field_formatter(field, format, view_mode, args)
		
		display_config = IN.fielder.field_display_config(field.entity_type, field.entity_bundle, view_mode, field.id)
		
		formatter_class = display_config.get('field_formatter', 'FieldFormatter')
		formatter_class = IN.fielder.formatter_class(formatter_class)
		
		config = display_config.get('field_formatter_config', {})
		
		# TODO: cache it
		formatter_obj = formatter_class()
		
		theme_output['content']['value'] = formatter_obj.format_value(field, format, view_mode, args, config)
		theme_output['content']['title'] = formatter_obj.format_title(field, format, view_mode, args, config)
		
		if theme_output['content']['value'] == '':
			field.visible = False
		
		field.css.append('field')
		field.css.append(field.__type__)
		field.css.append(field.name)
		

	def theme_process_variables(self, field, format, view_mode, args):
		super().theme_process_variables(field, format, view_mode, args)

		#field_config = IN.fielder.field_config(field.name)
		
	def theme_plateit(self, field, format, view_mode, args):
		if args is None:
			args = {}

		#output = self.__template__.safe_substitute(args)
		output = self.template_string.format_map(args)
		#output = self.template_string % args

		field.theme_current_output['output']['final'] = output

	#def theme_items(self, field, format, view_mode, args):
		#pass

builtins.Field = Field
