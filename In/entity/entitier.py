from .entity import *

class EntityTypes(dict):
	'''all Entity classes'''
	
	def __init__(self):
		
		for cls in IN.register.get_sub_classes_yield(Entity):
			self[cls.__type__] =  cls
		super().__init__()
		
	def __missing__(self, type):
		
		cls = IN.register.get_class(type, 'Entity')
		if cls is None:
			cls = Entity

		self[type] = cls
		return cls

class Entitiers(dict):
	'''all entity entitier classes'''

	def __missing__(self, type):
		
		cls = IN.register.get_class(type, 'Entity')
		if cls is None:
			cls = Entity

		self[type] = cls.Entitier
		return cls.Entitier



#********************************************************************
#					EntitierEngine
#********************************************************************	


class EntitierEngine:
	'''Entity controller

	Entity
		Entitier
		Model
	'''
	
	
	# some entities may be set this status for delete 
	STATUS_DELETED = -15
	
	def __init__(self):
		'''
		entity_bundle = {
			entity_type : {
				entity_bundle : {
					data : {},
				}
			}
		}
		'''
		
		# class cache
		IN.APP.static_cache['entity_class'] = {}
		
		self.entitiers = Entitiers()
		self.types = EntityTypes() 

		self.entity_bundle = RDict() #{} #OrderedDict() # RDict() recursive update
		self.build_entity_bundle()
		
		self.entity_model = RDict() # {}
		self.build_entity_model()
		
		
	def build_entity_bundle(self):

		config = self.entity_bundle

		# Update from In hook
		result = IN.hook_invoke('entity_bundle')
		
		for entities in result:
			
			for entity_type, bundles in entities.items():
				for entity_bundle, bundle_config in bundles.items():

					# update only if entity is available
					# if entity_type in self.types:
					try:
						config[entity_type][entity_bundle] = bundle_config
					except Exception as e:
						if entity_type not in config:
							config[entity_type] = {}
						config[entity_type][entity_bundle] = bundle_config

		try:
			# update from DB
			cursor = IN.db.execute('''SELECT *
				FROM config.config_entity_bundle
				ORDER BY entity_type
			''')
			
			if cursor.rowcount > 0:
				
				for row in cursor:
					entity_type = row['entity_type']
					entity_bundle = row['entity_bundle']
					data = row['data']
					try:
						bundle_config = config[entity_type][entity_bundle]
					except Exception as e:
						if entity_type not in config:
							config[entity_type] = {}
						if entity_bundle not in config[entity_type]:
							config[entity_type][entity_bundle] = {}
						bundle_config = config[entity_type][entity_bundle]

					if 'data' in bundle_config:
						bundle_config['data'].update(data)
					else:
						config[entity_type][entity_bundle]['data'] = data
					 
		except Exception as e:
			IN.logger.debug()
		
	def build_entity_model(self):
		'''build the entity data models'''

		models = IN.hook_invoke('entity_model')
		for model in models:
			self.entity_model.update(model)

		# lets other addons to alter
		models = IN.hook_invoke('entity_model_alter', self.entity_model)

		db_config = IN.db.__conn__.db_settings
		prefixes = db_config['table_prefix']
		
		entity_bundles = self.entity_bundle
		
		for type, model in self.entity_model.items():
			try:

				# set table prefix
				table = model['table']['name']
				prefix = prefixes.get(table, None) or prefixes.get('entity', None) or prefixes.get('default', '')

				# set the prefixed table name
				model['table']['name'] = prefix + table

				# moved as property in Model class
				
				# set the model config to entity models
				#entity_main_class = self.types[type]
				#entity_main_class.Model.model = model
				
				# each bundle may have different class
				#if type in entity_bundles:
					#for bundle in entity_bundles[type].keys():
						
						#bundle_class = entity_main_class.entity_class(type, bundle)
						#if bundle_class is not entity_main_class:
							#bundle_class.Model.model = model
				
			except Exception as e:
				IN.logger.debug()

	def load(self, type, id = None):
		'''Load entities of type

		type: type of the entity: nabar, content, profile

		id : int : load single entity
		id : None: load all entities
		id : any iterable: load multiple entities
		'''

		return self.types[type].Entitier.load(id)

	def load_single(self, type, id):
		'''load single entity'''
		return self.types[type].Entitier.load_single(id)

	def load_multiple(self, type, ids):
		'''load multiple entities'''

		return self.types[type].Entitier.load_multiple(ids)

	def load_all(self, type):
		'''load all entities'''

		return self.types[type].Entitier.load_all()

	def load_all_by_bundle(self, type, bundle):
		'''load all entities by bundle'''

		return self.types[type].Entitier.load_all_by_bundle(bundle)

	def select(self, type, where):
		'''load entities by where conditions'''

		return self.types[type].Entitier.select(where)

	def save(self, entity, commit = True):
		return entity.Entitier.save(entity, commit)

	def insert(self, entity, commit = True):
		return entity.Entitier.insert(entity, commit)

	def update(self, entity, commit = True):
		return entity.Entitier.update(entity, commit)

	def delete(self, entity, commit = True):
		return entity.Entitier.delete(entity, commit)

	def get_entity_add_form(self, entity_type, entity_bundle, args = None):
		'''returns EntityAddForm by entity_type and entity_bundle'''
		
		form = None
		try:
			
			entity_class = self.types[entity_type]
			form_type = entity_class.EntityAddForm.__type__

			if args is None:
				args = {}
				
			if 'data' not in args:
				args['data'] = {}
				
			# always pass entity type and bundle
			args['data']['entity_type'] = entity_type
			args['data']['entity_bundle'] = entity_bundle
			
			args['entity_type'] = entity_type
			args['entity_bundle'] = entity_bundle
			
			form = IN.former.load(form_type, args = args)

		except Exception as e:
			IN.logger.debug()

		return form
		

	def get_entity_edit_form(self, entity_type, entity_id, args = None):
		'''returns EntityEditForm by entity_type and entity_id'''
		
		form = None
		try:
			
			entity_class = self.types[entity_type]
			form_type = entity_class.EntityEditForm.__type__

			if args is None:
				args = {}
				
			if 'data' not in args:
				args['data'] = {}
				
			# always pass entity type and bundle
			args['data']['entity_type'] = entity_type
			args['data']['entity_id'] = entity_id
			
			form = IN.former.load(form_type, args = args)
			
			return form
		except Exception as e:
			IN.logger.debug()

		return None

	def get_entity_delete_form(self, entity, **args):
		'''returns EntityDeleteForm by entity_type and entity_id'''
		
		form = None
		try:
			
			form_type = entity.EntityDeleteForm.__type__

			# always pass entity type and bundle
			args['entity_type'] = entity.__type__
			args['entity_bundle'] = entity.type
			args['entity_id'] = entity.id
			
			form = IN.former.load(form_type, args = args)

		except Exception as e:
			IN.logger.debug()

		return form

	def access(self, op, entity_type, entity_bundle = None, account = None, deny = False):
		'''entity access shortcut'''

		context = IN.context
		if account is None:
			account = context.nabar

		result = self.__access__(op, entity_type, entity_bundle, account)
		
		if deny and not result:
			context.access_denied()

		return result
		
	def __access__(self, op, entity_type, entity_bundle, account):
		'''entity access shortcut'''
		
		entity_nabar_id = 0
		
		if not type(entity_type) is str:
			entity = entity_type
			entity_type = entity.__type__
			entity_bundle = entity.type
			entity_nabar_id = entity.nabar_id
			
		has_access = IN.nabar.access
		
		if has_access('admin_' + entity_type, account):
			return True

		
		entity_type_bundle = '_'.join((entity_type, entity_bundle))
		
		if has_access('admin_' + entity_type_bundle, account):
			return True

		# admin
		if op == 'admin':
			# admin access already checked
			return False
		
		# create / add
		if op == 'add':
		
			if has_access('add_' + entity_type_bundle, account):
				return True
			
			return False

		own = entity.nabar_id == account.id
		published = entity.status

		# TODO: anonymous to anomous, same nabar no edit/delete
		# view, edit, delete
		key = [op, entity_type_bundle]
		if own:
			key.append('own')
		else:
			key.append('others')
			
		if not published:
			key.append('unpublished')

		key = '_'.join(key)

		if has_access(key, account):
			return True
			
		return False


	def entity_page_view(self, entity_type, entity_id, view_mode, **args):

		# load the entity

		entity_id = int(entity_id)
		
		entity = self.load(entity_type, entity_id)

		context = IN.context
		
		if entity is None or entity.status == self.STATUS_DELETED:
			
			if view_mode == 'full': # display not found page only if it is full entity view
				context.not_found()
			return
			
		else:

			# display access denied page only it it is full entity view
			if view_mode == 'full':
				self.access('view', entity, deny = True)
			elif not self.access('view', entity, deny = False):
				return

			# invoke hooks
			
			# very heavy, dont implement this
			IN.hook_invoke('__entity_view__', entity)
			
			IN.hook_invoke('_'.join(('entity_view', entity.__type__)), entity)
			
			IN.hook_invoke('_'.join(('entity_view', entity.__type__, entity.type)), entity)

			# TODO: entity_type + bundle == entity + type_bundle
			
			context.ensure_page_response()

			# we use ThemeArgs to keep theme args, keep view mode now
			obj = ThemeArgs(entity, {'view_mode' : view_mode})
			context.response.output.add(obj)
			
			if view_mode == 'full':
				# set entity title
				title = self.entity_title(entity)
				if title:
					context.page_title = text = IN.texter.format(title, 'default')
		
		return entity
	
	def entity_page_edit(self, entity_type, entity_id, view_mode = 'full', **args):
		'''disply form to edit the entity
		
		view_mode: some time, we may need to display edit form 
		inside box, or other sections, so we dont need to redirect if no access
		view mode full is used to guess whether it is in main view
		'''
		entitier = IN.entitier
		context = IN.context
		
		# load the entity
		entity_id = int(entity_id)
		
		entity = entitier.load(entity_type, entity_id)
		
		if entity is None or entity.status == self.STATUS_DELETED:
		
			# invalid entity
			context.not_found()
			
		else:

			# access denied
			entitier.access('edit', entity, deny = True)
			
			context.ensure_page_response()

			try:
				# it may raise errors
				form = entitier.get_entity_edit_form(entity_type, entity_id)
				if form is not None:
					context.response.output.add(form)
			except Exception as e:
				IN.logger.debug()
				context.not_found()
			
			if view_mode == 'full':
				# set entity title
				title = self.entity_title(entity)
				if title:
					context.page_title = text = IN.texter.format(title, 'default')
		
		return entity
		
	def entity_page_delete(self, entity_type, entity_id, **args):
		'''disply form to edit the entity
		
		view_mode: some time, we may need to display edit form 
		inside box, or other sections, so we dont need to redirect if no access
		view mode full is used to guess whether it is in main view
		'''
		entitier = IN.entitier
		context = IN.context
		
		# load the entity
		entity_id = int(entity_id)
		
		entity = entitier.load(entity_type, entity_id)
		
		if entity is None or entity.status == self.STATUS_DELETED:
			# invalid entity
			context.not_found()
		else:

			# access denied
			entitier.access('delete', entity, deny = True)
			
			context.ensure_page_response()

			try:
				# it may raise errors
				form = entitier.get_entity_delete_form(entity)
				if form is not None:
					context.response.output.add(form)
			except Exception as e:
				IN.logger.debug()
				context.not_found()
			
			# set entity title
			title = self.entity_title(entity)
			if title:
				context.page_title = text = IN.texter.format(title, 'default')
		
		return entity
		
	def entity_title(self, entity):
		return entity.Entitier.entity_title(entity)
		
	def entity_context_links(self, entity, context_type, format, view_mode):

		return entity.Entitier.entity_context_links(entity, context_type, format, view_mode)
		
	def path(self, entity):
		return entity.Entitier.path(entity)
	
	def view_modes(self, entity_type, entity_bundle = ''):
		return self.types[entity_type].Entitier.view_modes(entity_bundle)
		
		
