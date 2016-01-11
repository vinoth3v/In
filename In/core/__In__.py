import logging.config
import greenlet

from In.core.logger import Logs
import In.core.register
import In.core.hooker
		

class IN:
	'''The IN Object.

	'''

	__version__ = (0, 5, 0)
	__root_path__ = None
	__In_debug__ = True
	
	# manually set custom context for some processes. 
	# be aware to change it once used.
	__context__ = None
	
	def __init__(self):

		# easy access
		self.hooker = In.core.hooker.INHooker()
		self.hook = self.hooker.hook
		self.hook_invoke = self.hooker.hook_invoke
		self.hook_invoke_yield = self.hooker.hook_invoke_yield

		self.register = In.core.register.INRegister()
		
		self.logger = Logs() # use default IN.logger config
		

	@property
	def root_path(self):

		if not self.__root_path__:
			self.__root_path__ = In.__path__[0]

		return self.__root_path__

	@property
	def debug(self):

		return self.__In_debug__

	@debug.setter
	def debug(self, mode):

		self.__In_debug__ = mode
	
	@property
	def context(self):
		'''returns the current greenlet context'''
		
		# hack
		if self.__context__:
			return self.__context__
		
		c = greenlet.getcurrent()
		return c
		
		# slow
		#while True:
			#try:
				#c.environ
				#return c
			#except:
				#try:
					#parent_c = c.parent
					
					#if parent_c == c:
						#raise Exception('Context not available!')
					#else:
						#c = parent_c
				#except:
					#return c
		
		#c.parent
		
		## it is contextpool
			
	
	#def context_switch(self):
		#'''run another context'''
		

class __INModuleNamespace__:
	'''The IN module namespace.'''

