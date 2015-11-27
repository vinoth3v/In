@IN.register('Comment', type = 'EntityEditForm')
class CommentEditForm(In.entity.EntityEditForm):
	'''Comment Edit Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		#self.id = '-'.join(('comment', str(self.entity.id), 'edit-form'))
		
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
		
		# TODO: skip validation
		set.add('Button', {
			'id' : 'cancel',
			'value' : s('cancel'),
			'css' : ['i-button ajax'],
			'attributes' : {
				'data-ajax_partial' : '1'
			}
		})
		
		self.css.append('ajax i-panel i-panel-box')

@IN.register('CommentEditForm', type = 'Former')
class CommentEditFormFormer(In.entity.EntityEditFormFormer):
	'''Comment Edit Form Former'''
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		entity = form.processed_data['entity']
		old_entity = form.processed_data['old_entity']
		
		entity.container_id = old_entity.container_id
		entity.parent_id = old_entity.parent_id
	
	def submit_partial(self, form, post):
		''''''
		
		if post['element_id'] == 'cancel':
			
			entity = form.entity
			
			element_id = '-'.join(('#comment', str(entity.id), 'children'))
			
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
		
		# no redirect after comment update
		form.redirect = None
		
		context = IN.context
		
		if not entity:
			context.not_found()
			
		#try:
		
		if context.request.ajax:
			element_id = '-'.join(('#comment', str(entity.id), 'children')) #form.id
			
			# theme children only
			
			# TODO: use parent themed format, view_mode
			themed_entity = IN.themer.theme(entity)			
			output = entity.theme_output['html']['default']['output']['children']
			
			form.result_commands = [{
				'method' : 'html',
				'args' : [element_id, output]
			}]
			#output = [{
				#'method' : 'replace',
				#'args' : [element_id, output]
			#}]
			#context.response = In.core.response.CustomResponse(output = output)
		
		else:
			# TODO: dymanic url based on entity view url
			context.redirect('/'.join((entity.parent_entity_type.lower(), str(entity.parent_entity_id))))
			
				
		#except Exception:
			#IN.logger.debug()


@IN.register('CommentEditForm', type = 'Themer')
class CommentEditFormThemer(FormThemer):
	'''CommentEditForm themer'''

	def theme(self, obj, format, view_mode, args):
		
		# chanage row size
		# TODO: move to admin field configuation
		if 'field_comment_body' in obj:
			for k, field in obj['field_comment_body'].items():
				if isinstance(field, In.html.tags.TextArea):
					field.rows = 1
		super().theme(obj, format, view_mode, args)
