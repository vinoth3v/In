import json

#import In.entity

class FlagType(In.entity.Entity):
	'''FlagType Entity class.
	'''

	def __init__(self, data = None, items = None, **args):
		
		self.data = {}
		
		super().__init__(data, items, **args)

@IN.register('FlagType', type = 'Entitier')
class FlagTypeEntitier(In.entity.EntityEntitier):
	'''Base FlagType Entitier'''

	# FlagType needs entity insert/update/delete hooks
	invoke_entity_hook = True

	entity_load_all = True
	entity_load_all_by_bundle = True
	
	
@IN.register('FlagType', type = 'Model')
class FlagTypeModel(In.entity.EntityModel):
	'''FlagType Model'''
	
	#not_updatable_columns = ['id', 'type', 'created', 
		#'actor_entity_type', 'actor_entity_id',
		#'target_entity_type', 'target_entity_id'
	#]

	def insert_prepare(self, entity, values):
		if 'data' in values:
			data = values['data']
			values['data'] = json.dumps(data, skipkeys = True, ensure_ascii = False)
		
	def update_prepare(self, entity, values):
		if 'data' in values:
			data = values['data']
			values['data'] = json.dumps(data, skipkeys = True, ensure_ascii = False)
		


@IN.hook
def entity_model():
	return {
		'FlagType' : {						# entity name
			'table' : {				# table
				'name' : 'flag_type',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'data' : {},
					'title' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('FlagType', type = 'Themer')
class FlagTypeThemer(In.entity.EntityThemer):
	'''FlagType themer'''


