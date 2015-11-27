@IN.register('Status', type = 'EntityEditForm')
class StatusEditForm(In.entity.EntityEditForm):
	'''Status Edit Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		#self.id = '-'.join(('status', str(self.entity.id), 'edit-form'))
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row'],
			'weight' : 50, # last
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Save'),
			'css' : ['i-button i-button-primary']
		})
		
		set.add('Button', {
			'id' : 'cancel',
			'value' : s('cancel'),
			'css' : ['i-button ajax'],
			'attributes' : {
				'data-ajax_partial' : '1'
			}
		})
		
		self.css.append('i-panel i-panel-box')

@IN.register('StatusEditForm', type = 'Former')
class StatusEditFormFormer(In.entity.EntityEditFormFormer):
	'''Status Edit Form Former'''
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		entity = form.processed_data['entity']
		old_entity = form.processed_data['old_entity']

	def submit_partial(self, form, post):
		''''''
		
		if post['element_id'] == 'cancel':
			
			entity = form.entity
			
			element_id = '-'.join(('#status', str(entity.id), 'children')) #form.id
			
			# theme children only
			
			# TODO: use parent themed format, view_mode
			themed_entity = IN.themer.theme(entity)			
			output = entity.theme_output['html']['default']['output']['children']
			
			form.result_commands = [{
				'method' : 'html',
				'args' : [element_id, output]
			}]
		
	def submit(self, form, post):
		'''Save the entity and return entity id'''
		
		entitier = IN.entitier
		entity = form.entity

		entitier.access('edit', entity, deny = True)
		
		super().submit(form, post)
		
		if form.has_errors:
			return
		
		# load the fresh entity
		entity = IN.entitier.load_single(entity.__type__, entity.id)
		
		# no redirect after status update
		form.redirect = None
		
		context = IN.context
		
		if not entity:
			context.not_found()
			
		#try:
		
		if context.request.ajax:
			element_id = '-'.join(('#status', str(entity.id), 'children')) #form.id
			
			# theme children only
			
			# TODO: use parent themed format, view_mode
			themed_entity = IN.themer.theme(entity)			
			output = entity.theme_output['html']['default']['output']['children']
			
			form.result_commands = [{
				'method' : 'html',
				'args' : [element_id, output]
			}]

		else:
			# TODO: dymanic url based on entity view url
			context.redirect('/'.join(('status', str(entity.id))))
			
			
		#except Exception:
			#IN.logger.debug()

