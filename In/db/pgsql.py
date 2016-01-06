
#TODO: asyncronous postgres
#import gevent_psycopg2; gevent_psycopg2.monkey_patch()

import psycopg2 as dbserver
import psycopg2.extras
import psycopg2.extensions
from psycopg2.extensions import POLL_OK, POLL_READ, POLL_WRITE, STATUS_PREPARED


'''

psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED
psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED			# default
psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ
psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE

'''
@IN.register('pgsql', type = 'theme_format')
class PGSQL(In.db.SQL):
	'''PGSQL Theme format class.

	'''
	
def wait_select(conn):
	
	while True:
		
		state = conn.poll()
		if state == POLL_OK:						# socket has data
			break
		elif state == POLL_READ:	
			IN.APP.context_pool.switch()		# run another event
		elif state == POLL_WRITE:
			IN.APP.context_pool.switch()		# run another event
		else:
			raise OperationalError("bad state from poll: %s" % state)

# set wait callback
#psycopg2.extensions.set_wait_callback(wait_select)
		

class PGSqlDBEngine(In.db.DBEngineBase):
	'''PGSql database engine class'''

	__db_type__ = 'pgsql'

	def __init__(self, db_settings):
		

		# it will call the connect
		super().__init__(db_settings)

	@property
	def connection(self):
		conn = self.__conn__
		if conn is None or not conn.status or conn.closed:
			# connect if not connected
			self.connect(activate = True)
		return conn

	@property
	def cursor(self):
		
		conn = self.connection
		cur = conn.cursor(cursor_factory = psycopg2.extras.DictCursor)
		
		return cur

	@property
	def closed(self):
		return self.__conn__.closed
		
	# method. not property
	def new_cursor(self, activate = True):
		'''Always creates a a new cursor'''
		if self.__conn__ is None or not self.__conn__.status:
			# connect if not connected
			self.connect(activate = True)
		cur = self.__conn__.cursor(cursor_factory=psycopg2.extras.DictCursor)
		if activate:
			self.__cursor__ = cur
		return cur

	def connect(self, *args, **kargs):
		# prepare connection string from settings

		#master = dict (
		#	db_type = 'pgsql',
		#	db_module = 'In.db.pgsql',
		#	db_class = 'PGSql',
		#	host = 'localhost',
		#	port = '',
		#	database = 'In_app',
		#	username = 'root',
		#	password = 'pgsql',
		#	table_prefix = dict (
		#		default = '', # default table prefix
		#	),
		#),

		self.__conn__ = dbserver.connect(
			host = self.db_settings['host'],
			database = self.db_settings['database'],
			user = self.db_settings['username'],
			password = self.db_settings['password'],
			port = self.db_settings['port'],
		)

		self.prepare_connection(self.__conn__)

		return self.__conn__

	def execute(self, sql, args = None):

		if type(sql) is not str: # query obj
			return sql.execute(args)
		
		c = self.cursor
			
		try:
			
			#IN.logger.debug(sql)
			
			c.execute(sql, args)
		
		except dbserver.Error as e:
			IN.logger.debug()
			
			# we rollback here, or it raises 
			# 'commands ignored until end of transaction block' error
			c.connection.rollback()
			
			raise e

		return c

	def execute_many(self, Q, *args, **kargs):
		return self.execute(Q, *args, **kargs)

	def execute_row(self, Q, *args, **kargs):
		return self.execute(Q, *args, **kargs)

	def execute_object(self, Q, *args, **kargs):
		'''Execute the Query object and returns the appropriated Object based on the first row.
		'''
		c = self.execute(Q, *args, **kargs)

		return c

	def execute_all(self, sql, *args, **kargs):
		return self.cursor.executemany(sql, *args, **kargs)

	def execute_later(self, sql, *args, **kargs):
		'''Accepts the parameters and return immediately without actually executing the query.

		This method is very useful for IN.logger-ing purpose without affecting performance overhead.
		Since it saves the parameters as it is, any references to it will be exists and changes on that will affect the parameters/query objects also.
		TODO: implement this.
		'''
		#we are saving the self object, Because we shouldn't execute the queries on other connections which are connected to other databases.
		self.__later_queries__.append([self, sql, args, kargs])

	def execute_script(self, sql, *args, **kargs):
		params = kargs
		c = self.cursor

		c.execute(sql, params)
		return c

	def rollback(self):
		'''Rollbacks the connection transactions.
		'''
		self.__conn__.rollback()

	def commit(self):
		'''Commits the connection transactions.
		'''
		self.__conn__.commit()

	def prepare_connection(self, conn):
		# set iso level
		conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED)
		IN.hook_invoke('db_prepare_connection', self)


	@staticmethod
	def sql_param_token(typ, key):
		#to use in the actual sql for parameter
		return ':' + key

	@staticmethod
	def query_param_token(typ, key):
		#to use inside query themer
		return ':' + str(key)

	def close(self):
		try:
			self.__conn__.close()
		except Exception as e:
			IN.logger.debug()


