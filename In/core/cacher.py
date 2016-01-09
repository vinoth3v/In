import pickle
import os
import base64
import hashlib
import urllib
import inspect
import shutil

from functools import *

from In.core.object_meta import ObjectMetaBase

class CacherException(Exception):
	'''Base Exception for Cacher related tasks.
	'''
	

class CacherContainer(dict):

	def __missing__(self, bin):
		
		cache_bins = IN.APP.config.cache_bins
		
		if bin in cache_bins: # mostly no
			bin_def = cache_bins[bin]
		else:
			try:
				# build from default CONFIG!
				bin_def = cache_bins['default']
			except KeyError:
				raise CacherException(s('Cache config for the bin $bin is undefined!', {'bin' : bin}))


		class_name = bin_def['cacher']
		args = bin_def.copy()
		del args['cacher']
		# caller will handle the error
		cls = IN.register.get_class(class_name, 'Cacher')

		self[bin] = cls(bin, **args)
		return self[bin]


class CacherEngine:

	# dict of all cacher instances APP scope.
	cachers = CacherContainer()

	def get(self, bin, key):
		return self.cachers[bin].get(key)

	def set(self, bin, key, value):
		return self.cachers[bin].set(key, value)

	def __getattr__(self, bin):
		'''Return the instance of the cacher configured for the cache bin.

		so, we can call it by IN.cacher.bin_name if needed.
		*** careful with bin names
		'''
		self.bin = self.cachers[bin]
		return self.bin
		
	def remove(self, bin, key): # del is simple :(, del is py keyword
		return self.cachers[bin].remove(key)

	def empty(self): # empty this cache bin # remove all
		return self.cachers[bin].empty()

#@IN.hook
#def __In_app_init__(app):
	### set the cacher
	#IN.cacher = CacherEngine()
	#IN.cacher.default # init default cache bin

	#IN.cacher.set('default', '11111::2222222', {'asdasd':'asdadas'})
	#pprint(IN.cacher.get('default', '11111::2222222'))


class CacherMeta(ObjectMetaBase):

	__class_type_base_name__ = 'CacherBase'
	__class_type_name__ = 'Cacher'


class CacherBase(metaclass = CacherMeta):
	'''Base class of all IN CacherBase.

	'''
	def get(self, key):
		''''''

	def set(self, key, value):
		''''''

	def remove(self, key): # del is simple :(, del is py keyword
		''''''

	def empty(self): # empty this cache bin # remove all
		''''''

@IN.register('Cacher', type = 'Cacher')
class Cacher(CacherBase):
	'''Base class of all IN CacherBase.

	'''
	def __init__(self, bin, **args):
		self.bin = bin
		
		if not self.bin or self.bin in ['/', '.', '..']:
			self.bin = 'default'
			raise RuntimeError('Unsafe Cache bin!')

class CacheFile(Cacher):
	'''Saves object to file.
	'''
	
	def __init__(self, bin, base_dir, digest = False):
		'''Initiate the File Cache.

		digest: false it if you are sure that cache keys will be "file name safe" for this cache bin.
		'''
		
		super().__init__(bin)
		
		if not base_dir or base_dir in ['/', '.', '..']:
			# security
			base_dir = os.path.join(IN.APP.config.tmp_file_dir, 'cache')
		
		# always add bin, so cahce keys will not be mixed up with
		# other bins if base path is default
		self.base_dir = os.path.join(base_dir, bin)	# base dir path for this bin
		self.digest = digest		# keys will be encoded

		self.memory_cache = {}
		
		self.digest_key = lru_cache(maxsize=9999)(self.digest_key)
		
		# TODO: profile save not working
		#self.get = lru_cache(maxsize = IN.APP.config.lru_cache_cache_file_max_limit)(self.get)
		

	def digest_key(self, key):
		return urllib.parse.quote_plus(key, '/', 'utf-8') # keep /
		#return base64.urlsafe_b64encode(key)
		#return hashlib.sha1(key).hexdigest() # performs near to md5

	def get(self, key):
		key = self.get_file_name(key)

		# in memory cache
		# TODO: MAX SIZE
		#try:
			#return self.memory_cache[key]
		#except KeyError:
			#pass
		result = self.__load__(key)
		#self.memory_cache[key] = result

		return result

	def get_file_name(self, key):
		key = str(key)
		this_path = key.replace(':', '/')
		
		#if self.digest:
			## TODO: digest only the last part?
			#this_path = self.digest_key(this_path)

		full_path = os.path.join(self.base_dir, this_path)

		# create dir if not exists
		os.makedirs(os.path.dirname(full_path), exist_ok = True)

		return full_path

	def __load__(self, file_name):
		'''Loads the file'''
		#if not os.path.exists(file_name):
			#return None
		try:
			with open(file_name, 'rb') as file:
				obj = pickle.load(file)				
				return obj
		except Exception as e:
			#curframe = inspect.currentframe()
			#calframe = inspect.getouterframes(curframe, 2)
			#pprint('caller name:', calframe)
			#print(traceback.format_exc())
			IN.logger.debug()
		return None

	def set(self, key, value):
		key = str(key)
		key = self.get_file_name(key)
		
		# TODO: MAX SIZE
		#self.memory_cache[key] = value
		
		return self.__write__(key, value)

	def __write__(self, file_name, value):
		'''write value to a file'''
		try:
			with open(file_name, 'wb') as file:
				pickle.dump(value, file, pickle.HIGHEST_PROTOCOL)
				return True
		except Exception as e:
			IN.logger.debug()
		return False

	def remove(self, key):
		key = str(key)
		
		key = self.get_file_name(key)
		
		try:
			if os.path.exists(key):
				os.remove(key)
		except Exception as e:
			IN.logger.debug()
	
	def remove_tree(self, key):
		'''dangerous'''
		
		key = str(key)
		
		key = self.get_file_name(key)
		
		try:
			shutil.rmtree(key, ignore_errors = True)
		except Exception as e:
			IN.logger.debug()
		
	