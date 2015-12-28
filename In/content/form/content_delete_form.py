@IN.register('Content', type = 'EntityDeleteForm')
class ContentDeleteForm(In.entity.EntityDeleteForm):
	'''Content Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : [''],
			'weight' : 50, # last
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'name' : 'submit',
			'value' : s('Delete'),
			'css' : ['i-button i-button-large i-button-danger']
		})

		set.add('Link', {
			'value' : s('Cancel'),
			'href' : '/' + self.entity.path(),
			'css' : ['i-button i-button-large']
		})
		

@IN.register('ContentDeleteForm', type = 'Former')
class ContentDeleteFormFormer(In.entity.EntityDeleteFormFormer):
	'''Content Form Former'''
	
	def submit(self, form, post):
		
		entity = form.entity
		
		if 'element_id' in post and post['element_id'] == 'submit':
			
			form.result_commands = []
			try:
				entity.Entitier.delete(entity)
			
				#form.redirect = '/'
				
				title = entity.Entitier.entity_title(entity) or ''
		
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('Content {title} has been deleted!', {'title' : title}),
						'status'  : 'info',
						'timeout' : 5000,
						'pos'     : 'bottom-left'			
					}]
				})
				
				form.result_commands.append({
					'method' : 'redirect',
					'args' : ['/', True]
				})
				
			except Exception as e:
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('Unable to delete!'),
						'status'  : 'info',
						'timeout' : 5000,
						'pos'     : 'bottom-left'			
					}]
				})
		

@IN.register('ContentDeleteForm', type = 'Themer')
class ContentDeleteFormThemer(FormThemer):
	'''ContentDeleteForm themer'''


