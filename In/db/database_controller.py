import importlib
import random

#from In.db.database_model_wrapper import *


class DatabaseController:
	'''Database Controller class to act as a wrapper for multiple connections, and other database related objects.

	'''
	
	
	__conn__ = None # active database connection
	__cursor__ = None

	def __init__(self, db_settings = None, **args):

		# TODO :
		#

		# assigning Database object to IN Application
		#self.db_model = DatabaseModelWrapper()

		self.connections = {}
		self.free_connections = []

		# use the default db_settings
		if db_settings is None:
			db_settings = IN.APP.config.db_settings

		self.db_settings = db_settings

		# initiate the target strings
		for main_name, server_conf in self.db_settings.items() :
			for server_name, db_conf in server_conf.items() :

				# import the db modules
				importlib.import_module(db_conf['db_module'])

				# now get the database class instance.
				db_class = In.util.raw_eval('.'.join((db_conf['db_module'], db_conf['db_class'])))
				

				target = ':'.join((main_name, server_name))
				self.connections[target] = None

	@property
	def connection(self):
		conn = self.__connection__
		
		if conn.connection.isexecuting() or conn.connection.closed:
			# connection is in use or closed
			# create a new one
			conn = self.connect(activate = False)
			
		return conn
		
	
	@property
	def __connection__(self):
		''' DB connection and cursor are not greenlet safe'''
		
		context = IN.context
		try:
			
			for conn in context.db_connections:
				if conn and not conn.closed and not conn.__conn__.isexecuting():
					return conn
				
		except AttributeError:
			# context not initiated
			# use global conn
			conn = self.__conn__
			if conn and not conn.closed:
				return conn
			conn = self.connect(activate = True)
			return conn
		
		conn = None
		
		while self.free_connections:
			conn = self.free_connections.pop()
			if not conn or conn.closed:
				conn = None
			else:
				break
			
		if conn is None:
			# create new connection
			conn = self.connect(activate = False)
			
		context.db_connections.append(conn)
		return conn #.connection
		

	@property
	def cursor(self):
		return self.connection.cursor

	## method. not property
	#def new_cursor(self, activate = True):
		#'''Creates a new cursor'''
		#return self.__conn__.new_cursor()

	def connect(self, target = None, activate = True):
		'''connect function.

		target : target of the db settings which it connect to.
		It will use a random settings and return the connection.
		if you want to connect to a specific db settings,
		you have to first add the configuration to db settings with
		a target keys, and pass that key here to get the connection.

		activate : By default it set the new connection as active.
		So you have to pass activate = Fase if you just need
		a connection and don't want it set to active.
		'''

		if type(target) is str:

			conn = self.__connect__(target)
			if activate:
				self.__conn__ = conn

			return conn

		else:

			# first, select from app db settings randomly
			db_random_target = random.choice([k for k in self.connections.keys()])

			try:

				conn = self.__connect__(db_random_target)
				if activate:
					self.__conn__ = conn

				return conn

			except Exception as e1:
				
				# IN.logger the error
				# TODO: send notification mail?

				IN.logger.debug()

				# retry all one by one.
				for db_target, dummy in self.connections.items():
					try:

						if db_target == db_random_target: # we tried it and failed
							continue

						conn = self.__connect__(db_target)
						if activate:
							self.__conn__ = conn

						return conn

					except Exception as e:
						
						IN.logger.debug()
						pass

			# if Nothing helps, raise error
			#raise In.db.DBConnectionFailedException()

	def __connect__(self, target, reconnect = False):
		'''Connect to appropriate Database'''

		# reuse the existing connection for the specific target
		# TODO: force reconnect if connection is broken.
		#if not reconnect and target in self.connections and self.connections[target]:
		#	return self.connections[target]

		parts = target.split(':')
		
		settings = self.db_settings[parts[0]][parts[1]]

		db_class = In.util.raw_eval('.'.join((settings['db_module'], settings['db_class'])))
		
		conn = db_class(settings)

		self.connections[target] = conn

		return conn

	#def __getattr__(self, name):
		#'''Shortcut method to call DBEngine methods from DBController.

		#'''

		#attr = getattr(self.__conn__, name)
		##setattr(self.__conn__, name, attr)

		#return attr

	def execute(self, sql, args = None):
		
		conn =  self.connection
		
		return conn.execute(sql, args)

	def select(self, json):
		return In.db.Select(json)

	def insert(self, json):
		return In.db.Insert(json)

	def update(self, json):
		return In.db.Update(json)

	def delete(self, json):
		return In.db.Delete(json)

	def free(self, context):
		'''Free / reuse the connections'''
		
		if not context.db_connections:
			return
		
		conn = context.db_connections.pop()
		if conn:
			self.free_connections.append(conn)
			
			try:
				# rollback
				conn.rollback()
			except Exception as e:
				IN.logger.debug()
				
				
		# close others
		for conn in context.db_connections:
			try:
				conn.close()
			except Exception as e:
				IN.logger.debug()
		
		
		