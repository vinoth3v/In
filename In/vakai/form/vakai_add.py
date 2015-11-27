@IN.register('Vakai', type = 'EntityAddForm')
class VakaiAddForm(In.entity.EntityAddForm):
	'''Vakai Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)

		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary'],
			'weight' : 50, # last
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Save'),
			'css' : ['i-button i-button-primary']
		})

		self.add('HTMLSelect', {
			'id' : 'weight',
			'value' : post.get('weight', 0),
			'title' : s('Weight'),
			'options' : range(100),
			'required' : True,
			'multiple' : False,
			'css' : ['i-form-large'],
			'weight' : 10,
		})
		
		self.css.append('ajax i-panel i-panel-box')
		
@IN.register('VakaiAddForm', type = 'Former')
class VakaiAddFormFormer(In.entity.EntityAddFormFormer):
	'''Vakai Form Former'''
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		args =  form.args
		
		parent_entity_type = args['parent_entity_type']
		parent_entity_bundle = args['parent_entity_bundle']
		
		if 'parent_entity_id' in args:
			#parent_entity_bundle = args['parent_entity_bundle']
			parent_entity_id = args['parent_entity_id']
			
			entity = form.processed_data['entity']
			
			parent_field_name = entity.Entitier.parent_field_name
			if parent_field_name in entity:
				entity[parent_field_name].value = {
					'' : {
						0 : {
							'value' : parent_entity_id
						}
					}
				}
		

	def submit(self, form, post):

		super().submit(form, post)
		
		if form.has_errors:
			return
		
		form.redirect = None # prevent redirect
		
		args =  form.args
		
		parent_entity_type = args['parent_entity_type']
		parent_entity_bundle = args['parent_entity_bundle']
		
		parent_entity_id = 0
		if 'parent_entity_id' in args:
			parent_entity_id = args['parent_entity_id']
			
		# set result commands
		if form.entity_id is not None:
			vakai = IN.entitier.load('Vakai', form.entity_id)
			
			if vakai is not None:
				output = IN.themer.theme(vakai, view_mode = 'adminlist')
				
				element_id = '_'.join(('VakaiListLazy', parent_entity_type, parent_entity_bundle, str(parent_entity_id)))
				#print(element_id)
				form.result_commands = [{
					'method' : 'append',
					'args' : ['#' + element_id, output]
				}]
				
				# TODO: reset fields
				
@IN.register('VakaiAddForm', type = 'Themer')
class VakaiAddFormThemer(FormThemer):
	'''VakaiAddForm themer'''
