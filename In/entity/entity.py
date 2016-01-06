
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
	
	@property
	def deleted(self):
		'''has deleted status'''
		return self.status == IN.entitier.STATUS_DELETED
	

builtins.Entity = Entity
