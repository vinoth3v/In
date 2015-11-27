@IN.register('Status', type = 'EntityDeleteForm')
class StatusDeleteForm(In.entity.EntityDeleteForm):
	'''Status Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-modal-footer i-text-right'],
			'weight' : 50, # last
		})
		
		set.add('Link', {
			'name' : 'cancel',
			'value' : s('Cancel'),
			'css' : ['i-button i-modal-close']
		})
		
		set.add('Submit', {
			'id' : 'submit',
			'name' : 'submit',
			'value' : s('Delete'),
			'css' : ['i-button i-button-danger']
		})

		self.css.append('i-panel')

@IN.register('StatusDeleteForm', type = 'Former')
class StatusDeleteFormFormer(In.entity.EntityDeleteFormFormer):
	'''Status Form Former'''
	
	def submit(self, form, post):
		
		entity = form.entity
		
		form.result_commands = [{
			'method' : 'closeAjaxModal',
			'args' : [],
		}]
		
		if 'submit' in post:
			try:
				entity.Entitier.delete(entity)
			
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('Status deleted!'),
						'status'  : 'info',
						'timeout' : 5000,
						'pos'     : 'bottom-left'			
					}]
				})
			
				form.result_commands.append({
					'method' : 'remove',
					'args' : ['.Status.Status-' + str(form.entity.id)]
				})
			except Exception as e:
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('Unable to delete this status!'),
						'status'  : 'info',
						'timeout' : 5000,
						'pos'     : 'bottom-left'			
					}]
				})
		else:
			form.result_commands.append({
				'method' : 'notify',
				'args' : [{
					'message' : s('Unable to delete this status!'),
					'status'  : 'info',
					'timeout' : 5000,
					'pos'     : 'bottom-left'			
				}]
			})
			

@IN.register('StatusDeleteForm', type = 'Themer')
class StatusDeleteFormThemer(FormThemer):
	'''StatusDeleteForm themer'''

