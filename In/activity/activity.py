
#import In.entity

class Activity(In.entity.Entity):
	'''Activity Entity class.
	'''
	
	viewed = False
	def __init__(self, data = None, items = None, **args):

		# default
		self.nabar_id = 0
		
		super().__init__(data, items, **args)


@IN.register('Activity', type = 'Entitier')
class ActivityEntitier(In.entity.EntityEntitier):
	'''Base Activity Entitier'''

	# Activity needs entity insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = False
	
@IN.register('Activity', type = 'Model')
class ActivityModel(In.entity.EntityModel):
	'''Activity Model'''


@IN.hook
def entity_model():
	return {
		'Activity' : {						# entity name
			'table' : {				# table
				'name' : 'activity',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'viewed' : {},
					'changed' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('Activity', type = 'Themer')
class ActivityThemer(In.entity.EntityThemer):
	'''Activity themer'''


	def theme(self, obj, format, view_mode, args):
		super().theme(obj, format, view_mode, args)
		
		obj.css.append('i-margin-bottom')


	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		
		
		
