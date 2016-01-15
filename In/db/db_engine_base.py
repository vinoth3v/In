


class DBEngineBase:
	'''Base class for all DB Engine Implementations.
	'''

	__db_type__ = 'base_engine'

	__conn__ = None
	__cursor__ = None

	db_settings = None

	sql_ops = dict (
		eq      = '=',
		le      = '<=',
		lt      = '<',
		ge      = '>=',
		gt      = '>',
		ne      = '!=',
		like    = 'LIKE',
		exists  = 'EXISTS',
	)
	
	has_changes = False
	
	def __init__(self, db_settings):

		self.__conn__ = None
		self.__cursor__ = None
		self.db_settings = db_settings

		self.connect()


	@property
	def connection(self):
		return self.__conn__

	@property
	def db_type(self):
		return self.__db_type__

	def connect(self, *args, **kargs):
		pass

	@property
	def cursor(self):
		if self.__cursor__ is None:
			if self.__conn__ is None or not self.__conn__.status:
				self.connect(activate = True)
			else:
				self.__cursor__ = self.__conn__.cursor()
		return self.__cursor__

	# method. not property
	def new_cursor(self, activate = True):
		'''Creates a new cursor'''
		if self.__cursor__ is None:
			if self.__conn__ is None or not self.__conn__.status:
				self.connect(activate = True)
				cur = self.__conn__.cursor()
			else:
				cur = self.__conn__.cursor()
		if activate:
			self.__cursor__ = cur
		return cur

	def execute(self, sql, args = None):
		pass

	def execute_all(self, sql, *args, **kargs):
		pass

	def execute_add_queue(self, sql, *args, **kargs):
		pass

	def prepare_connection(self, conn):
		pass

	@staticmethod
	def sql_param_token(typ, key, val):
		#to use in the actual sql for parameter
		return str(key)

	@staticmethod
	def query_param_token(typ, key):
		#to use inside te query themer
		return ':' + str(key)





