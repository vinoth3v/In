

class ObjectMismatchException(Exception):
	'''Exception ObjectMismatchException.
	'''


class Object(ObjectBase):
	'''The IN Object class.

	'''

	info = ''
	help = ''
	tooltip = ''

	prefix = None
	suffix = None

	item_wrapper   = None
	child_separator  = None
	child_wrapper  = None
	theme_output     = None		# contains all formats rendered output
	validation_rule = None			# valuator rules
	has_errors = None

	value = None
	def_value = ''
	title = ''
	visible    = True
	weight = None

	# theme specific, per instance
	default_children_view_mode = None

	def __init__(self, data = None, items = None, **args):

		if data is None: data = {}
		if items is None: items = {}

		if 'id' not in data:
			data['id'] = '_'.join((self.__type__, str(id(self))))

		if 'name' not in data:
			data['name'] = str(data['id'])

		self.css = []
		self.attributes = {} #OrderedDict()
		self.validations = []

		super().__init__(data, items, **args)

		## init default children # use __init___ override
		#self.__init__children__()

##    def __repr__(self):
##        return self.theme('html')
##
##    def __str__(self):
##        return self.theme('text')

	def get_attributes(self):
		return self.attributes

	def add(self, obj = None, type = 'Object', **args):
		'''Add a Object to Object dict.'''

		bType = builtins.type
		obj_type = type

		if bType(obj) is str:
			# use first string as string
			obj_type = obj

		if bType(type) is dict:
			# second arg may be dict
			data = type
			args['data'] = data


		if not isinstance(obj, Object):

			#if 'weight' not in args:
				#args['weight'] = len(self)
			try:
				obj = self.new(obj_type, **args)
			except Exception as e1:
				IN.logger.debug()

		if obj is not None and isinstance(obj, self.__allowed_children__ or self.__default_child__ or Object):
			#print('old ', obj.id, obj.weight)
			if obj.weight is None:
				obj.weight = len(self)
				#print('new ', obj.id, obj.weight)
			self[obj.id] = obj

			return obj
		else:
			pass
			#print(3333333333, obj.__class__, self.__allowed_children__, self.__default_child__)

		# Raise Exception
		raise ObjectMismatchException(''.join(('Unable to add item to ', str(self.__class__), '. Allowed values: Object. Got: ', str(bType(obj)))))



	#@staticmethod
	#def __pos_cmp__(o,p):
		#'''Compares two Objects by its Position.

		#'''
		#return cmp(o.weight, p.weight)

	#def _set_attrs(self, prop, setdef = False, dval='' ):
		#try:
			#if hasattr(self, prop) and getattr(self, prop):
				#self.attributes[prop] = getattr(self,prop)
			#elif setdef:
				#self.attributes[prop] = dval
		#except Exception as e:
			#print(str(e) + traceback.format_exc())
			#if setdef:
				#self.attributes[prop] = dval

##    def _setProperty1(self, key, dval='', prop='', sargs={}):
##        if not prop:
##            prop = key
##        if sargs:
##            pargs = sargs
##        else:
##            pargs = self.args
##
##        try:
##            if pargs:
##                if key in pargs:
##                    setattr(self, prop, pargs[key])
##                else:
##                    setattr(self, prop, dval)
##            else:
##                setattr(self, prop, dval)
##        except Exception as e:
##            IN.logger.add_error(str(e))
##        #print(prop , getattr(self, prop))

	def getval(self):
		return self.value or self.def_value or ''

	#def validate(self):
		#return  self.__validate__() and \
			#all(IN.hook_invoke('item_validate_' + self.type , self)) and \
			#self.validate_items()

	#def validate_items(self):
		#return all(itm.validate() for itm in self.values())

	#def __validate__(self):

		#if self.validations:
			#try:
				#return all( f(self) for f in self.validations)
			#except Exception as e:
				#IN.logger.add_error(str(e))
				#return False
		#return True


	def get_item(self, id, recursive=True):
		'''Object.get_item
		Search through the children and returns the child by id.

		id = id of the item
		rec = recursive search?
		'''
		ret = self.get(id, None)
		if ret:
			return ret
		if recursive:
			for itm in self.values():
				ret = itm.get_item(id, recursive)
				if ret:
					return ret
		return None

	#def get_items(self, rec=True, **args):
		#'''Object.get_item
		#Search through the children and returns the children by the given key value.

		## TODO: USE yield?
		#rec = recursive search?
		#'''

		#itms = OrderedDict()
		#for key, val in args.items():
			#for itm in self.values():
				#if hasattr(itm, key) and getattr(itm, key) == val:
					#itms[itm.id] = itm
		#if rec:
			#for itm in self.values():
				#ret = itm.get_items(rec, **args)
				#if ret:
					#itms.update(ret)
		#return itms

	def copy(self):
		# TODO: update attributes?
		obj = self.__class__.__new__(self.__class__)
		obj.__dict__.update(self.__dict__)
		return obj


	@staticmethod
	def new(type, *pargs, **kargs):
		'''Helper function to create appropriate type of object.

		'''

		#try:
			#builder = kargs['__builder__']
			#obj = builder(*pargs, **kargs)
			#return obj
		#except KeyError as e:
			#pass #suppress key error
			##print(str(e) + traceback.format_exc())

		# get the class type
		objclass = IN.register.get_class(type, 'Object')

		if objclass is None:
			# use the default
			objclass = Object

		obj = objclass(*pargs, **kargs)

		return obj


	#def __del__(self):
		##del self.theme_output
		#self.theme_output = None


class Text(Object):
	pass

builtins.Object = Object
builtins.Text = Text
