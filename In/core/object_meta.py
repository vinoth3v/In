

class ObjectMetaBase(type):

	__class_type_base_name__ = ''
	__class_type_name__ = ''

	def __new__(meta_class, name, bases, dict):

		obj = type.__new__(meta_class, name, bases, dict)

		obj.__type_alias__ = obj.__dict__.get('__type_alias__', obj.__name__)

		# v test commented __class_extenders__
		#if not hasattr(obj, '__class_extenders__'):
			#obj.__class_extenders__ = {} #OrderedDict()

		#__update = obj.__class_extenders__.update

		#for base in bases:
			#try:
				#if hasattr(base, '__class_extenders__'):
					#__update(base.__class_extenders__)
			#except Exception:
				#IN.logger.debug()
				
				
		#if issubclass(obj, ObjectBase):
		if name != meta_class.__class_type_base_name__:
			# we don't want ObjectBase to be registered as 'Object'
			# it may give 'type is not defined' error before loading ObjectBase class defined below

			IN.register.register_class(obj, name, 'Object')
			
			# register also as that purticular type name
			if meta_class.__class_type_name__ != 'Object':
				IN.register.register_class(obj, name, meta_class.__class_type_name__)
				

		try:
			if hasattr(obj, '__allowed_children__'):
				if type(obj.__allowed_children__) is list  and 'self' in obj.__allowed_children__:
					allowed_classes = [cls for cls in obj.__allowed_children__ if type(cls) is str and cls != 'self']
					allowed_classes.append(obj)
					obj.__allowed_children__ = allowed_classes
		except Exception as e:
			IN.logger.debug()


		## use default css classes
		#if name in IN.APP.config.default_css:
			#obj.__default_css__ = IN.APP.config.default_css[name]

		return obj

	@property
	def __type__(self):
		'''This type property returns type of the class

		'''
		return self.__type_alias__ or self.__name__

class ObjectMeta(ObjectMetaBase):

	__class_type_base_name__ = 'ObjectBase'
	__class_type_name__ = 'Object'


class ObjectBase(dict, metaclass = ObjectMeta):
	'''Base class of all IN custom object classes.

	'''
	
	__allowed_children__ = None
	__default_child__ = None
	__default_css__ = None

	@property
	def __type__(self):
		return self.__type_alias__ or self.__class__.__type__


	def __init__(self, data = None, items = None, **args):

		if data is None: data = {}
		if items is None: items = {}

		super().__init__(items)

		self.track				= False
		self.item_wrapper		= None
		self.child_separator	= None
		self.child_wrapper		= None
		self.theme_output		= None


		# this will overrite existing & default data members
		for name, value in data.items():
			try:
				setattr(self, name, value) 	# may raise error
			except Exception as e:
				IN.logger.debug(e)
				raise e

		#if items:
			#allowed_classes = self.__allowed_children__ or self.__default_child__ or ObjectBase
			#for name, value in items.items():
				#if isinstance(value, allowed_classes):
					#self[name] = value
				##try:  # ignoe if already exists?
					##_t = self[name]
				##except KeyError:


	def __bool__(self):
		'''always True for if obj'''
		return True

builtins.ObjectMeta = ObjectMeta
builtins.ObjectBase = ObjectBase
