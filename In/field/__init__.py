from .field import *
from .field_type import *
from .field_formatter import *
from .admin import *

class FieldException(Exception):
	'''Base Field Exception
	'''
	
class FieldExceptionInvalidField(FieldException):
	'''InvalidField'''

@IN.register
def register():
	'''
	instance :
		class - class type assigned directly
		instance - instance will be created and assigned, all object will use the same member instance
	'''
	return {
		# all field type class should have Fielder member of type which is
		'class_members' : {								# register for
			'Field' : {								# type of object - arg to class members
				'Fielder' : {						# key
					'name' : 'Fielder',			# member name
					'instance' : 'instance',			# type of instance
				},
				'Model' : {							# key
					'name' : 'Model',				# member name
					'instance' : 'instance',			# type of instance
				},
			},
			'FieldFormatter' : {								# type of object - arg to class members
				'FieldFormatterConfigForm' : {					# key
					'name' : 'FieldFormatterConfigForm',			# member name
					'instance' : 'class',				# type of instance
				},
			},
		},
	}


@IN.hook
def entity_field_config():

	config = {}

	try:

		cursor = IN.db.execute('''SELECT * FROM config.config_entity_field c
			where status = 1 ORDER BY weight''')

		if cursor.rowcount == 0:
			return {}

		for row in cursor:

			entity_type = row['entity_type']
			entity_bundle = row['entity_bundle']
			field_type = row['field_type']
			field_name = row['field_name']
			weight = row['weight']
			data = row['data']

			if entity_type not in config:
				config[entity_type] = {}

			entity = config[entity_type]

			if entity_bundle not in entity:
				entity[entity_bundle] = {}

			field_config = entity[entity_bundle]

			field_config[field_name] = {
				'field_type' : field_type,
				'field_name' : field_name,
				'weight' : weight,
				'data' : data,
			}

	except Exception as e:
		IN.logger.debug()

	
	return config
