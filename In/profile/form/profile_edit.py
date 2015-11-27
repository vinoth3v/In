@IN.register('Profile', type = 'EntityEditForm')
class ProfileEditForm(In.entity.EntityEditForm):
	'''Profile Edit Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)

		set = self.add('FieldSet', {
			'id' : 'adminset',
			'css' : ['i-form-row i-text-primary'],
			'weight' : 100,
		})
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-text-primary'],
			'weight' : 101, # last
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Save'),
			'css' : ['i-button i-button-primary i-button-large']
		})

		self.css.append('ajax i-panel i-panel-box i-margin-large')

@IN.register('ProfileEditForm', type = 'Former')
class ProfileEditFormFormer(In.entity.EntityEditFormFormer):
	'''Profile Edit Form Former'''

	def submit(self, form, post):
		super().submit(form, post)
		
		entity = form.processed_data['entity']
		
		if entity.id is not None:
			
			if IN.context.request.path_parts[0] == 'nabar':
				
				form.redirect = None # no redirect
			
				form.result_commands = []
			
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('Profile saved!'),
						'status'  : 'info',
						'timeout' : 5000,
						'pos'     : 'bottom-left'			
					}]
				})
			
		
