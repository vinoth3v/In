
#import In.entity

class Flag(In.entity.Entity):
	'''Flag Entity class.
	'''
	
	actor_entity_type = ''
	actor_entity_id = 0
	target_entity_type = ''
	target_entity_id = 0
	flag_status = ''
	
	def __init__(self, data = None, items = None, **args):

		super().__init__(data, items, **args)

@IN.register('Flag', type = 'Entitier')
class FlagEntitier(In.entity.EntityEntitier):
	'''Base Flag Entitier'''

	# Flag needs entity insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = False
	entity_load_all_by_bundle = False
	
	
	
@IN.register('Flag', type = 'Model')
class FlagModel(In.entity.EntityModel):
	'''Flag Model'''
	
	not_updatable_columns = ['id', 'type', 'created', 
		'actor_entity_type', 'actor_entity_id',
		'target_entity_type', 'target_entity_id'
	]


@IN.hook
def entity_model():
	return {
		'Flag' : {						# entity name
			'table' : {				# table
				'name' : 'flag',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'flag_status' : {},
					'nabar_id' : {},
					'actor_entity_type' : {},
					'actor_entity_id' : {},
					'target_entity_type' : {},
					'target_entity_id' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('Flag', type = 'Themer')
class FlagThemer(In.entity.EntityThemer):
	'''Flag themer'''


