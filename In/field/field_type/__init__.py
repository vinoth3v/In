
from .text import *
from .textarea import *
from .number import *
from .entity_reference import *
from .text_select import *
from .number_select import *
from .date import *

from .admin import *

@IN.hook
def field_model():
	# default model
	return {
		'default' : {								# field type
			'columns' : {							# table columns
				'id' : {'type' : 'bigserial'},
				'entity_type' : {'type' : 'varchar', 'length' : 64},
				'entity_id' : {'type' : 'bigint'},
				'language' : {'type' : 'varchar', 'length' :  4, 'default' : 'lang'},
				'weight' : {'type' : 'smallint'},
				'value' : {'type' : 'text'}, 		# value type based on field type
				'created' : {},
			},
			'keys' : {
				'primary' : 'id',
			},
		},
	}
