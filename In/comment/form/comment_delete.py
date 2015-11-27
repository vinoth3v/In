@IN.register('Comment', type = 'EntityDeleteForm')
class CommentDeleteForm(In.entity.EntityDeleteForm):
	'''Comment Form'''
	
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

@IN.register('CommentDeleteForm', type = 'Former')
class CommentDeleteFormFormer(In.entity.EntityDeleteFormFormer):
	'''Comment Form Former'''
	
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
						'message' : s('Comment deleted!'),
						'status'  : 'info',
						'pos'     : 'bottom-left'			
					}]
				})
			
				form.result_commands.append({
					'method' : 'remove',
					'args' : ['.Comment.Comment-' + str(form.entity.id)]
				})
			except Exception as e:
				form.result_commands.append({
					'method' : 'notify',
					'args' : [{
						'message' : s('Error while deleting this comment!'),
						'status'  : 'info',
						'pos'     : 'bottom-left'			
					}]
				})
		else:
			form.result_commands.append({
				'method' : 'notify',
				'args' : [{
					'message' : s('Unable to delete this comment!'),
					'status'  : 'info',
					'pos'     : 'bottom-left'			
				}]
			})
			

@IN.register('CommentDeleteForm', type = 'Themer')
class CommentDeleteFormThemer(FormThemer):
	'''CommentDeleteForm themer'''


