
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
		if self.__cacher__:
			return self.__cacher__
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
			except Exception:
				IN.logger.debug()
			
			# clear by bundle
			try:
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
		
		result = entity.Model.update(entity, commit)

		# clear single
		try:
			self.cacher.remove(entity.id)
		except Exception:
			IN.logger.debug()
		
		# clear all
		try:
			if self.entity_load_all:
				self.cacher.remove('all')
		except Exception:
			IN.logger.debug()
		
		# clear by bundle
		try:
			if self.entity_load_all_by_bundle:
				self.cacher.remove(entity.type)
		except Exception:
			IN.logger.debug()
		
		# clear theme cache	
		try:
			theme_cacher = entity.ThemeCacher
			if theme_cacher.theme_cache_enabled:
				theme_cacher.remove_all_by_obj(entity)
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
		except Exception:
			IN.logger.debug()
		
		try:
			if self.entity_load_all:
				self.cacher.remove('all')
		except Exception:
			IN.logger.debug()
		
		try:
			if self.entity_load_all_by_bundle:
				self.cacher.remove(entity.type)
		except Exception:
			IN.logger.debug()
			
		# clear theme cache	
		try:
			theme_cacher = entity.ThemeCacher
			if theme_cacher.theme_cache_enabled:
				theme_cacher.remove_all_by_obj(entity)
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

