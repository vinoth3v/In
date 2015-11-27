
#import In.entity

class Content(In.entity.Entity):
	'''Content Entity class.
	'''
	
	featured = False
	
	#def __init__(self, data = None, items = None, **args):

		#super().__init__(data, items, **args)


@IN.register('Content', type = 'Entitier')
class ContentEntitier(In.entity.EntityEntitier):
	'''Base Content Entitier'''

	# Content needs entity insert/update/delete hooks
	invoke_entity_hook = True

	# load all is very heavy
	entity_load_all = False
	
	def path(self, entity):
		''''''
		return '/'.join(('node', str(entity.id)))
	
@IN.register('Content', type = 'Model')
class ContentModel(In.entity.EntityModel):
	'''Content Model'''
	
	set_deleted_status = True

@IN.hook
def entity_model():
	return {
		'Content' : {						# entity name
			'table' : {				# table
				'name' : 'content',
				'columns' : {		# table columns / entity attributes
					'id' : {},
					'type' : {},
					'created' : {},
					'status' : {},
					'nabar_id' : {},
					'featured' : {},
				},
				'keys' : {
					'primary' : 'id',
				},
			},
		},
	}

@IN.register('Content', type = 'Themer')
class ContentThemer(In.entity.EntityThemer):
	'''Content themer'''


	def theme(self, obj, format, view_mode, args):
		super().theme(obj, format, view_mode, args)
		
		obj.css.append('i-margin-bottom')
		
		if obj.featured:
			obj.css.append('featured')
		
		obj.css.append('i-margin')
	

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)
		
		nabar = IN.entitier.load('Nabar', obj.nabar_id)
		
		args['nabar_name'] = nabar.name
		args['nabar_id'] = nabar.id
		args['nabar_picture'] = IN.nabar.nabar_profile_picture_themed(nabar)
		
		
		if obj.featured:
			args['featured'] = s('Featured post').join(('<span class="i-badge i-badge-success i-float-right"><i class="i-icon-bookmark"></i> ', '</span>'))
		else:
			args['featured'] = ''
			
