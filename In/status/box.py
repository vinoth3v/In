

class BoxStatusAddForm(In.boxer.BoxLazy):
	
	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
		
		# always set new id
		self.id = 'BoxStatusAddForm_nabar_status'
		if IN.context.request.ajax_lazy:
			
			entitier = IN.entitier
			entity_type = 'Status'
			entity_bundle = 'nabar_status'
			# access denied
			if not entitier.access('add', entity_type, entity_bundle, deny = False):
				return
			
			form_args = {}
			if 'to_entity_type' in args:
				form_args['to_entity_type'] = args['to_entity_type']
			else:
				form_args['to_entity_type'] = 'Nabar'
			
			if 'to_entity_id' in args:
				form_args['to_entity_id'] = args['to_entity_id']
			else:
				form_args['to_entity_id'] = IN.context.nabar.id
				
			form = entitier.get_entity_add_form(entity_type, entity_bundle, form_args)

			if form is not None:
				self.add(form)
			
			self.add('TextDiv', {
				'id' : 'status_added_list',
				'weight' : 10,
			})

@IN.register('BoxStatusAddForm', type = 'Themer')
class BoxStatusAddFormThemer(In.boxer.BoxLazyThemer):
	''''''
	
