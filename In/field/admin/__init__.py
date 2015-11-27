from .action import *
from .page import *
from .form import *
from .hook import *

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
				'FieldConfigForm' : {						# key
					'name' : 'FieldConfigForm',			# member name
					'instance' : 'class',			# type of instance
				},
			},
		},
	}
