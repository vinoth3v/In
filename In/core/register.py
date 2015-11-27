from collections import defaultdict

class INRegister:
	'''IN register class'''
	
	registration_disabled = False
	
	registered_functions = []
	registered_classes = []
	
	sdict = lambda: defaultdict(list)
	registered_classes_sorted = defaultdict(sdict)
	
	def __call__(self, *args, type = 'Object'):
		'''IN register class
	
		@IN.register('Content', type = 'EntityAddForm')
		class ContentAddForm(EntityAddForm):
			# form to be added as EntityAddForm for Content
			pass
		
		
		@IN.register
		def register():
			# register function to be called later
			return {}
			
		'''

		if self.registration_disabled:
			return args[0]

		# return the hook function that handles the register later
		if builtins.type(args[0]) is not str:
			# it is register function	
			if  hasattr(args[0], '__name__') and \
				hasattr(args[0], '__kwdefaults__') and \
				args[0].__name__ == 'register':
				
				self.register_function(args[0])
				
				return args[0]

			return args[0]

		
		if builtins.type(args[0]) is str:
			name = args[0]
			
			def hook_func(cls):
				self.register_class(cls, name, type)
				return cls
				
			return hook_func

		return args[0]
		
	
	def register_function(self, register_function):
		
		self.registered_functions.append(register_function)
		
	def register_class(self, register_class, register_for, register_as = 'Object'):
		if register_class not in self.registered_classes:
			self.registered_classes.append(register_class)
		
		register_class.__register_for__ = register_for
		register_class.__register_as__ = register_as
		
		register_for_dict = self.registered_classes_sorted[register_for]
		register_for_dict[register_as].append(register_class)
		
	def process_registers(self):
		'''process all register functions'''
		
		for function in self.registered_functions:
			
			try:
				result = function()
			except Exception as e:
				continue
			
			if 'class_members' not in result:
				return
				
			class_members = result['class_members']
			
			
			for register_for, register_as_def in class_members.items():
				for register_as, register_def in register_as_def.items():
					
					register_for_class = self.get_class(register_for, 'Object')
					
					if not register_for_class:
						continue
						
					register_as_class = self.get_class(register_for, register_as)
					
					if register_as_class:
						
						if register_def['instance'] == 'instance':
							try:
								register_as_class_obj = register_as_class(register_for_class, register_def['name'], register_as)
							except Exception as e1:
								continue
						else:
							register_as_class_obj = register_as_class
						
						setattr(register_for_class, register_def['name'], register_as_class_obj)
					
					# process sub classes
					for sub_class in self.registered_classes:
						if not issubclass(sub_class, register_for_class):
							continue
						
						register_as_class = self.get_class(sub_class.__type__, register_as)
						
						if not register_as_class:
							continue
						if register_def['instance'] == 'instance':
							try:
								register_as_class_obj = register_as_class(sub_class, register_def['name'], register_as)
							except Exception as e1:
								IN.logger.debug()
								continue
						else:
							register_as_class_obj = register_as_class
						
						setattr(sub_class, register_def['name'], register_as_class_obj)
					
					
	def get_class(self, class_name, type = 'Object'):
		'''return the class that is registered as type'''
		
		try:
			classes = self.registered_classes_sorted[class_name][type]
			if classes:
				return classes[-1] # return lastest registered
		except Exception as e:
			return None
	
	def get_sub_classes_yield(self, base_class):
		'''yield all sub classes of base class'''
		
		# TODO: cache it?
		for sub_class in self.registered_classes:
			if issubclass(sub_class, base_class):
				yield sub_class
	
	def get_sub_classes(self, base_class):
		'''return all sub classes of base class'''
		
		return [field for field in self.get_sub_classes(base_class)]
	
	
	
	
