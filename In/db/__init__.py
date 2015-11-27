__all__ = ['query']


from In.db.database_controller import *
#from In.db.database_model_wrapper import *

from In.db.db_engine_base import *

from In.db.query import *

@IN.register('sql', type = 'theme_format')
class SQL(In.themer.TEXT):
	'''SQL Theme fotmat class
	'''


@IN.register('DBException', type = 'exception_handler')
class DBException(Exception):
	'''Base Exception for all database related errors.
	'''

	#def handle_exception(self, context):
		#pass

@IN.register('DBConnectionFailedException', type = 'exception_handler')
class DBConnectionFailedException(DBException):
	'''Exception DBConnectFailedException.
	'''

@IN.register('DBObjectUnknownTypeException', type = 'exception_handler')
class DBObjectUnknownTypeException(DBException):
	'''Exception DBObjectUnknownTypeException.
	'''

@IN.register('DBEngineInitializationException', type = 'exception_handler')
class DBEngineInitializationException(DBException):
	'''Exception DBEngineInitializationException.
	'''


class DBTableUnknownTypeException(DBException):
	'''Exception DBTableUnknownTypeException.
	'''

class DBArgumentException(DBException):
	'''Exception DBArgumentException.
	'''

class DBColumnNotFoundException(DBException):
	'''Exception DBColumnNotFoundException.
	'''


@IN.register
def register():

	return {
		'class_members' : {
			'db_table' : {
				'__query_builder__' : {
					'name' : '__query_builder__',
					'instance' : 'instance', # class, instance, perobject, whether the member is instance or class
				},
				'__db_controller__'  : {
					'name' : '__db_controller__',
					'instance' : 'instance', # class, instance, perobject, whether the member is instance or class
				},
			},
		},
	}

# default columns
columns = {
	'id' : { 'type' : 'bigserial', },
	'type' : { 'type' : 'varchar', 'length' : 64, },
	'status' : { 'type' : 'smallint', },
	'created' : { 'type' : 'timestamp', },
	'changed' : { 'type' : 'timestamp', },
}



