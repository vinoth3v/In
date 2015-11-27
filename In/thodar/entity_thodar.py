
#import In.entity

class Thodar(In.entity.Entity):
	'''Thodar Entity class.
	'''
	
	entity_type = ''
	entity_id = 0
	
	#def __init__(self, data = None, items = None, **args):

		#super().__init__(data, items, **args)


@IN.register('Thodar', type = 'Entitier')
class ThodarEntitier(In.entity.EntityEntitier):
	'''Base Thodar Entitier'''

	# Thodar needs entity insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = False
	
@IN.register('Thodar', type = 'Model')
class ThodarModel(In.entity.EntityModel):
	'''Thodar Model'''


@IN.register('Thodar', type = 'Themer')
class ThodarThemer(In.entity.EntityThemer):
	'''Thodar themer'''


@IN.hook
def entity_model():
	return {
		'Thodar' : {				# entity name
			'table' : {				# table
				'name' : 'thodar',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'entity_type' : {},
					'entity_id' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}
