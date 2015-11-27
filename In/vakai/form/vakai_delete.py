@IN.register('Vakai', type = 'EntityDeleteForm')
class VakaiDeleteForm(In.entity.EntityDeleteForm):
	'''Vakai Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-modal-footer i-text-right'],
			'weight' : 50, # last
		})
		
		set.add('Submit', {
			'name' : 'submit',
			'value' : s('Delete'),
			'css' : ['i-button i-button-danger']
		})
		
		set.add('Link', {
			'name' : 'cancel',
			'value' : s('Cancel'),
			'css' : ['i-button i-modal-close']
		})
		
		self.css.append('ajax i-panel')

@IN.register('VakaiDeleteForm', type = 'Former')
class VakaiDeleteFormFormer(In.entity.EntityDeleteFormFormer):
	'''Vakai Form Former'''
	
	def submit(self, form, post):
		
		entity = form.entity
		
		form.result_commands = [{
			'method' : 'closeAjaxModal',
			'args' : [],
		}]
		
		if 'submit' in post:
			
			entity.Entitier.delete(entity)
			
			form.result_commands.append({
				'method' : 'notify',
				'args' : [{
					'message' : s('Vakai deleted!'),
					'status'  : 'info',
					'timeout' : 5000,
					'pos'     : 'bottom-left'			
				}]
			})
			
			form.result_commands.append({
				'method' : 'remove',
				'args' : ['.Vakai.vakai-' + str(form.entity.id)]
			})


@IN.register('VakaiDeleteForm', type = 'Themer')
class VakaiDeleteFormThemer(FormThemer):
	'''VakaiDeleteForm themer'''

