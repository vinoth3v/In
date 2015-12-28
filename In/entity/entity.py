import json
import datetime


#********************************************************************
#					ENTITY
#********************************************************************


class EntityMeta(ObjectMeta):

	__class_type_base_name__ = 'EntityBase'
	__class_type_name__ = 'Entity'

class EntityBase(Object, metaclass = EntityMeta):
	'''Base class of all IN Entity.

	'''
	__allowed_children__ = None
	__default_child__ = None
	

class Entity(EntityBase):
	'''Base Entity class.

	-- to define class specific to entity bundle

	@IN.register('Content', type = 'page')
	class ContentPage(Content):
		pass

	@IN.register('Content', type = 'article')
	class ContentArticle(Content):
		pass
	--

	'''

	type = ''
	nabar_id = 0
	status = 0

	@property
	def user_id(self):
		'''alias to nabar_id'''
		return self.nabar_id

	@user_id.setter
	def user_id(self, id):
		self.nabar_id = id

	def __init__(self, data = None, items = None, **args):
		if data is None:
			data = {}

		if 'created' not in data:
			# IN.context is not available here
			# nabar entity is creating on Context.__init__
			data['created'] = datetime.datetime.now()

		# status based on bundle config
		#data['status'] = data.get('status', 1) # published

		# entity bundle
		if 'type' not in data:
			# default to entity type
			data['type'] = self.__type__


		super().__init__(data, items, **args)

		if 'status' not in data:
			try:
				self.status = IN.entitier.entity_bundle[self.__type__][self.type]['data']['default_status']
			except Exception as e:
				#IN.logger.debug()
				self.status = 1 # published as default

		#if 'nabar_id' not in data:
			#data['nabar_id'] = IN.context.nabar.id

		# entity ids are numeric
		if type(self.id) is str:
			if self.id.isnumeric():
				self.id = int(self.id)
			else:
				self.id = None # new entity


		# TODO: build entity fields

	@classmethod
	def entity_class(cls, entity_type, entity_bundle):
		'''helper function that returns the class of the entity'''

		cache = IN.APP.static_cache['entity_class']

		try:
			return cache[entity_type][entity_bundle]
		except KeyError as e:
			pass

		register = IN.register
		objclass = Entity

		# get the class for Entity bundle
		objclass = register.get_class(entity_type, entity_bundle)
		if objclass is None:
			# get the class type for Entity
			objclass = register.get_class(entity_type, 'Entity')

		# mem cache it
		if entity_type not in cache:
			cache[entity_type] = {}
		cache[entity_type][entity_bundle] = objclass

		return objclass

	@classmethod
	def new(cls, type, data, items = None, **kargs):
		'''Overrides Object.new to get object of type Entity.

		'''
		entity_type = type

		# set the bundle if not set
		try:
			bundle = data['type']
		except KeyError as e:
			bundle = entity_type
			data['type'] = bundle

		objclass = cls.entity_class(entity_type, bundle)

		if items is None:
			items = {}

		obj = objclass(data, items, **kargs)

		# Add fields to entity
		fielder = IN.fielder

		if entity_type in fielder.entity_field_config:

			entity_config = fielder.entity_field_config[entity_type]

			bundle = obj.type

			# get field names for this bundle
			if bundle in entity_config:
				field_config = entity_config[bundle]

				for key, field in field_config.items():
					field_name = field['field_name']
					field_type = field['field_type']

					field_data = {}
					if field_name in data:
						field_data['value'] = data[field_name]
					else:
						field_data = {}

					# reverse reference
					field_data['entity'] = obj

					field_data['entity_type'] = entity_type
					field_data['entity_bundle'] = bundle
					field_data['id'] = field_name
					field_data['field_name'] = field_name
					field_data['field_type'] = field_type

					field_class = fielder.field_types[field_type]

					field_obj = field_class(field_data)
					obj.add(field_obj)

		return obj

	# easy methods
	def save(self, commit = True):
		return self.Entitier.save(self, commit)

	def insert(self, commit = True):
		return self.Entitier.insert(self, commit)

	def update(self, commit = True):
		return self.Entitier.update(self, commit)

	def delete(self, commit = True):
		return self.Entitier.delete(self, commit)

	def path(self):
		return self.Entitier.path(self)


#********************************************************************
#					ENTITY Entitier
#********************************************************************


class EntityEntitierBase:
	'''Base entity Entitier class'''

@IN.register('Entity', type = 'Entitier')
class EntityEntitier(EntityEntitierBase):
	'''Base Entity Entitier'''

	
	#entity_type = 'Entity'

	# some entities dont need to invoke these hooks
	invoke_entity_hook = False

	# should load all entities of this type?
	# heavy. dont not True it for Content, comments like entitites
	# TODO:
	entity_load_all = True
	entity_load_all_by_bundle = True

	title_field_name = 'field_title'

	view_modes_cache = {}

	def __init__(self, objcls, key, mem_type):
		self.entity_class = objcls
		self.entity_type = objcls.__type__

		# cacher is not available here
		#self.cacher = IN.cacher.cachers['entity_' + self.entity_type]
		self.__cacher__ = None

	@property
	def cacher(self):
		if self.__cacher__ is None:
			self.__cacher__ = IN.cacher.cachers['entity_' + self.entity_type]
		return self.__cacher__

	def entity_title(self, entity):

		#if not entity:
			#return ''

		title_field_name = self.title_field_name

		if title_field_name in entity:
			try:
				return entity[title_field_name].value[''][0]['value']
			except Exception as e:
				IN.logger.debug()
		
		return ': '.join((entity.__type__, str(entity.id)))

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
		'''load single entity

		'''

		if not id:
			raise In.entity.EntityException(s("Invalid entity id '{id}' of type {type}!", {'id' : str(id), 'type' : self.entity_type}))

		# use the cache
		# TODO: load/cache by language

		entity = self.cacher.get(id)

		if entity is not None:
			return entity

		# load from DB
		entity_data = self.entity_class.Model.load_single(id)

		if entity_data is None:
			return None

		#obj = self.entity_class(entity_data)
		entity = self.entity_class.new(self.entity_class.__type__, entity_data)

		# load entity fields
		db_loaded = {entity.id : entity}
		self.__load_add_entity_fields__(db_loaded)

		self.load_entity_additional_data(entity)

		if self.invoke_entity_hook:
			IN.hook_invoke('_'.join(('entity_load', entity.__type__, entity.type)), entity)
			IN.hook_invoke('entity_load_' + entity.__type__, entity)

			# heavy. dont implement
			IN.hook_invoke('__entity_load__', entity)

		# set the cache
		self.cacher.set(id, entity)

		return entity

	def load_multiple(self, ids):
		'''load multiple entities

		'''

		loaded = {}

		# use cache
		for id in ids:
			obj = self.cacher.get(id)
			if obj is not None:
				loaded[obj.id] = obj

		ids = set(ids) - set(loaded.keys())

		if not ids:
			return loaded

		ids = list(ids)

		# load data from db
		db_loaded = self.entity_class.Model.load_multiple(ids)

		if db_loaded:
			# initiate the Entities
			for id, entity_data in db_loaded.items():
				try:
					# initiate the entity
					#entity = self.entity_class(entity_data)
					entity = self.entity_class.new(self.entity_class.__type__, entity_data)
					db_loaded[id] = entity
				except Exception as e:
					IN.logger.debug()


			## add fields
			self.__load_add_entity_fields__(db_loaded)


			for id, entity in db_loaded.items():
				if entity:

					self.load_entity_additional_data(entity)

					if self.invoke_entity_hook:
						IN.hook_invoke('_'.join(('entity_load', entity.__type__, entity.type)), entity)
						IN.hook_invoke('entity_load_' + entity.__type__, entity)

						# heavy. dont implement
						IN.hook_invoke('__entity_load__', entity)

					# set the cache
					self.cacher.set(id, entity)

			loaded.update(db_loaded)

		return loaded

	def load_all(self):
		'''load all entities

		'''

		if not self.entity_load_all:
			return None

		# use the cache
		obj = self.cacher.get('all') # 'all' is special and heavy
		if obj is not None:
			return obj

		# model.select only returns ids
		ids = self.entity_class.Model.select([])

		if ids is None:
			return None

		db_loaded = self.load_multiple(ids)

		# set the cache
		if db_loaded:
			self.cacher.set('all', db_loaded)

		return db_loaded

	def load_all_by_bundle(self, bundle):
		'''load all entities by bundle

		'''

		if not self.entity_load_all_by_bundle:
			return None

		# use the cache
		obj = self.cacher.get(bundle) # bundle is special and heavy
		if obj is not None:
			return obj

		# model.select only returns ids
		ids = self.entity_class.Model.select([['type', bundle]])

		if ids is None:
			return None

		db_loaded = self.load_multiple(ids)

		# set the cache
		if db_loaded:
			self.cacher.set(bundle, db_loaded)

		return db_loaded

	def __load_add_entity_fields__(self, entities):
		'''load and add fields to entities

		entities : dict of entities
		'''

		fielder = IN.fielder
		entity_type = self.entity_class.__type__

		if entity_type in fielder.entity_field_config:

			entity_config = fielder.entity_field_config[entity_type]

			# group entity ids by bundle
			bundles = {}
			for id, entity in entities.items():
				if entity.type not in bundles:
					bundles[entity.type] = []

				bundles[entity.type].append(id)

			for bundle, ids in bundles.items():
				# get field names for this bundle
				if bundle in entity_config:
					field_config = entity_config[bundle]

					for key, field in field_config.items():
						field_name = field['field_name']
						field_type = field['field_type']
						weight = field['weight']
						title = field['data'].get('title', '')

						# load from DB
						field_data = fielder.load(entity_type, field_type, ids, field_name)

						if not field_data:
							continue
						for returned_id, field_obj in field_data.items():
							# add field to entity
							field_obj.weight = int(weight)
							field_obj.title = title

							# bundle is not available in table
							field_obj.entity_bundle = entities[returned_id].type

							# reverse reference
							field_obj.entity = entities[returned_id]

							entities[returned_id].add(field_obj)


	def select(self, where):
		'''load entities by where conditions'''

		if not self.entity_load_all and where is None:
			return None

		# model.select only returns ids
		ids = self.entity_class.Model.select(where)

		if ids is None:
			return None

		return self.load_multiple(ids)

	def load_entity_additional_data(self, entity):
		'''load_entity_additional_data'''
		entity.Model.load_entity_additional_data(entity)

	def save(self, entity, commit = True):
		if entity.id:
			return self.update(entity, commit)
		else:
			return self.insert(entity, commit)

	def insert(self, entity, commit = True):

		# cache will be set on next load
		result = entity.Model.insert(entity, commit)

		if result:

			# clear the all cache
			try:
				if self.entity_load_all:
					self.cacher.remove('all')
				if self.entity_load_all_by_bundle:
					self.cacher.remove(entity.type)
			except Exception:
				IN.logger.debug()

			# hook invoke
			if self.invoke_entity_hook:
				IN.hook_invoke('_'.join(('entity_insert', entity.__type__, entity.type)), entity)
				IN.hook_invoke('entity_insert_' + entity.__type__, entity)

			# heavy. dont implement
			IN.hook_invoke('__entity_insert__', entity)

		return result

	def update(self, entity, commit = True):
		
		print('111111111111111111111111, ENTITY UPDATED : ', entity.__type__, entity.type, entity.id, entity.nabar_id)
		
		result = entity.Model.update(entity, commit)

		# clear the cache

		try:
			self.cacher.remove(entity.id)
			if self.entity_load_all:
				self.cacher.remove('all')
			if self.entity_load_all_by_bundle:
				self.cacher.remove(entity.type)
		except Exception:
			IN.logger.debug()

		# hook invoke
		if self.invoke_entity_hook:
			IN.hook_invoke('_'.join(('entity_update', entity.__type__, entity.type)), entity)
			IN.hook_invoke('entity_update_' + entity.__type__, entity)

		# very heavy. dont implement
		IN.hook_invoke('__entity_update__', entity)

		return result

	def delete(self, entity, commit = True):

		result = entity.Model.delete(entity, commit)

		# clear the cache
		try:

			self.cacher.remove(entity.id)
			if self.entity_load_all:
				self.cacher.remove('all')
			if self.entity_load_all_by_bundle:
				self.cacher.remove(entity.type)

		except Exception:
			IN.logger.debug()

		# hook invoke
		if self.invoke_entity_hook:
			IN.hook_invoke('_'.join(('entity_delete', entity.__type__, entity.type)), entity)
			IN.hook_invoke('entity_delete_' + entity.__type__, entity)

		# heavy. dont implement
		IN.hook_invoke('__entity_delete__', entity)

		return result

	def entity_context_links(self, entity, context_type, format, view_mode):
		output = {}

		entitier = IN.entitier

		# no view access
		if not entitier.access('view', entity):
			return


		id_suffix = '-'.join((entity.__type__, str(entity.id)))

		if context_type == 'links':
			pass
			#if entitier.access('edit', entity):

				#edit = Object.new(type = 'Link', data = {
					#'id' : 'edit-link-' + id_suffix,
					#'css' : ['ajax i-button i-button-small'],
					#'value' : s('edit'),
					##'href' : s('#'),
					#'weight' : 0,
				#})
				#output[edit.id] = edit

			#if entitier.access('delete', entity):

				#edit = Object.new(type = 'Link', data = {
					#'id' : 'delete-link-' + id_suffix,
					#'css' : ['ajax i-button i-button-small'],
					#'value' : s('delete'),
					##'href' : s('#'),
					#'weight' : 1,
				#})
				#output[edit.id] = edit

		# hook alter
		IN.hook_invoke('_'.join(('entity_context_links', entity.__type__, entity.type)), entity, context_type, output, format, view_mode)
		IN.hook_invoke('entity_context_links_' + entity.__type__, entity, context_type, output, format, view_mode)
		# heavy. dont implement
		IN.hook_invoke('__entity_context_links__', entity, context_type, output, format, view_mode)

		#(self, entity, context_type)

		return output

	def view_modes(self, entity_bundle = ''):


		# update from db
		if entity_bundle:
			if entity_bundle in self.view_modes_cache:
				return self.view_modes_cache[entity_bundle]

			view_modes = self.entity_class.Themer.view_modes()

			try:
				modes = IN.entitier.entity_bundle[self.entity_type][entity_bundle]['data']['view_modes']
				for m in modes:
					view_modes.add(m)
			except KeyError as e:
				view_modes = {'default', 'full', 'teaser'} # default

			IN.hook_invoke('entity_view_modes_alter', self.entity_type, view_modes, entity_bundle)
			self.view_modes_cache[entity_bundle] = view_modes

			return view_modes

		else:

			if entity_bundle in self.view_modes_cache:
				return self.view_modes_cache['']

			view_modes = self.entity_class.Themer.view_modes()

			# merge all view modes
			for bundle, bundle_config in IN.entitier.entity_bundle[self.entity_type].items():
				try:
					modes = bundle_config['data']['view_modes']
					for m in modes:
						view_modes.add(m)
				except KeyError as e:
					pass

			IN.hook_invoke('entity_view_modes_alter', self.entity_type, view_modes, entity_bundle)
			self.view_modes_cache[''] = view_modes
			return view_modes


	def path(self, entity):
		'''return the path of this entity'''
		return '/'.join((entity.__type__.lower(), str(entity.id)))

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


#********************************************************************
#					ENTITY Themer
#********************************************************************


@IN.register('EntityBase', type = 'Themer')
class EntityBaseThemer(In.themer.ObjectThemer):

	theme_tpl_type = 'tpl.py'

	def view_modes(self):
		modes = super().view_modes()
		modes.add('full')
		return modes

	#def theme(self, obj, format, view_mode, args):
		#pass

	#def theme_done(self, obj, format, view_mode, args):
		#pass

	#def theme_items(self, obj, format, view_mode, args):
		#pass

	#def theme_process_variables(self, obj, format, view_mode, args):
		#pass

@IN.register('Entity', type = 'Themer')
class EntityThemer(EntityBaseThemer):


	def view_modes(self):
		modes = super().view_modes()
		modes.add('teaser')
		return modes

	def theme_prepare(self, obj, format, view_mode, args):

		# order the entity fields for this display config, view mode

		# TODO: move to separate function?
		fielder = IN.fielder
		entity_type = obj.__type__
		entity_bundle = obj.type

		if entity_type not in fielder.entity_field_config:
			# entity type not found
			return

		entity_config = fielder.entity_field_config[entity_type]

		if entity_bundle not in entity_config:
			return

		field_config = entity_config[entity_bundle]

		for key, field in field_config.items():

			if key not in obj:
				# field not found in entity
				continue

			field_name = field['field_name']
			default_weight = field['weight']
			weight = default_weight

			display_config = fielder.field_display_config(entity_type, entity_bundle, view_mode, field_name)

			if 'field_formatter_config' in display_config and 'weight' in display_config['field_formatter_config']:
				weight = display_config['field_formatter_config']['weight']

			obj[key].weight = weight

	def theme_attributes(self, obj, format, view_mode, args):
		obj.css.append(obj.__type__)
		obj.css.append('view-mode-' + view_mode)
		obj.css.append('-'.join((obj.__type__, str(obj.id))))
		obj.css.append('-'.join((obj.__type__, obj.type)))
		super().theme_attributes(obj, format, view_mode, args)

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)

		data = {
			'lazy_args' : {
				'load_args' : {
					'data' : {
						'parent_entity_type' : obj.__type__,
						'parent_entity_id' : obj.id,
						'theme_view_mode' : view_mode
					},
				},
			},
			'parent_entity_type' : obj.__type__,
			'parent_entity_id' : obj.id,
			'weight' : 10,
			'theme_view_mode' : view_mode,
		}

		link = Object.new('EntityContextLinks', data)
		menu = Object.new('EntityContextMenu', data)
		tab = Object.new('EntityContextTab', data)

		theme = IN.themer.theme
		args['entity_context_links'] = theme(link, format, 'lazy')
		args['entity_context_menu'] = theme(menu, format, 'lazy')
		#args['entity_context_tab'] = theme(tab, format, 'lazy')

		if obj.created:
			# lang
			st = obj.created.strftime
			args['created'] = ' '.join((s(st('%B')), st("%d, %Y %I:%M"), s(st('%p'))))

		args['entity_id'] = obj.id

class EntityContextLinks(In.core.lazy.HTMLObjectLazy):

	context_type = 'links'

	theme_view_mode = 'default'

	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)

		parent_entity_type = self.parent_entity_type
		parent_entity_id = self.parent_entity_id

		# always set new id
		self.id = '_'.join((self.__type__, parent_entity_type, str(parent_entity_id), self.theme_view_mode))

		# TODO:
		#self.css.append('')

class EntityContextMenu(EntityContextLinks):

	context_type = 'menu'

class EntityContextTab(EntityContextLinks):

	context_type = 'tab'


@IN.register('EntityContextLinks', type = 'Themer')
class EntityContextLinksThemer(In.core.lazy.HTMLObjectLazyThemer):


	def theme_items(self, obj, format, view_mode, args):

		if view_mode != 'lazy':

			entitier = IN.entitier

			# add entity links here
			entity_type = obj.parent_entity_type
			entity_id = obj.parent_entity_id

			entity = entitier.load_single(entity_type, entity_id)

			if entity is not None:

				links = entitier.entity_context_links(entity, obj.context_type, format, obj.theme_view_mode)

				if links is not None:
					for id, l in links.items():
						obj.add(l)

			super().theme_items(obj, format, view_mode, args)


builtins.Entity = Entity
