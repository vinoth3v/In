
class ObjectThemeCacherBase:
	'''ObjectThemeCacherBase class.'''
	
	# TODO: allow in config
	theme_cache_enabled = False # default

@IN.register('Object', type = 'ThemeCacher')
class ObjectThemeCacher(ObjectThemeCacherBase):
	''''''
	
	def __init__(self, objcls, key, mem_type):
		''''''
		
		self.object_class = objcls
		self.object_type = objcls.__type__
		
		self.__cacher__ = None

	@property
	def cacher(self):
		if self.__cacher__:
			return self.__cacher__
		
		self.__cacher__ = IN.cacher.cachers['ThemeCache_' + self.object_type]
		return self.__cacher__

	def get(self, obj, format, view_mode, args):
		'''return cached them output'''
		
		key = self.get_cache_key(obj.__type__, obj.id, format, view_mode, args)
		
		return self.cacher.get(key)
	
	def get_by_id(self, type, id, format, view_mode, args):
		'''useful to get cache without obj loading'''
		
		key = self.get_cache_key(type, id, format, view_mode, args)
		
		return self.cacher.get(key)
	
	def set(self, obj, output, format, view_mode, args):
		'''set cached them output'''
		
		key = self.get_cache_key(obj.__type__, obj.id, format, view_mode, args)
		
		return self.cacher.set(key, output)
		
	def set_by_id(self, type, id, output, format, view_mode, args):
		'''useful to set cache without obj loading'''
		
		key = self.get_cache_key(type, id, format, view_mode, args)
		
		return self.cacher.set(key, output)
	
	def remove_all_by_obj(self, obj):
		'''remove all cache of obj'''
		
		# we may need to remove entire dir of obj when updating
		
		key = ':'.join((obj.__type__, str(obj.id)))
		
		try:
			self.cacher.remove_tree(key)
		except Exception:
			IN.logger.debug()
	
	
	def get_cache_key(self, type, id, format, view_mode, args):
		'''return cache key for this obj'''
		
		context = args.get('context', None) or IN.context
		
		language = args.get('language', None) or context.language
		
		if not language:
			language = 'ta'
		
		theme_name = context.current_theme.__name__
		
		# we may need to remove entire dir of obj when updating
		
		return ':'.join((type, str(id), theme_name, format, view_mode, language, 'cache'))
	
	def process_cached_output(self, obj, cached_result, format, view_mode, args):
		'''allows themecacher to post process cached output'''
		return cached_result
	