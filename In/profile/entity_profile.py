
#import In.entity

class Profile(In.entity.Entity):
	'''Profile Entity class.
	'''

	def __init__(self, data = None, items = None, **args):

		# default
		self.nabar_id = 0
		
		super().__init__(data, items, **args)



@IN.register('Profile', type = 'Entitier')
class ProfileEntitier(In.entity.EntityEntitier):
	'''Base Profile Entitier'''

	# Profile needs entity insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = False
	
@IN.register('Profile', type = 'Model')
class ProfileModel(In.entity.EntityModel):
	'''Profile Model'''


@IN.hook
def entity_model():
	return {
		'Profile' : {						# entity name
			'table' : {				# table
				'name' : 'profile',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('Profile', type = 'Themer')
class ProfileThemer(In.entity.EntityThemer):
	'''Profile themer'''

	def theme(self, obj, format, view_mode, args):
		super().theme(obj, format, view_mode, args)
		
		obj.css.append('i-panel i-panel-box')
		