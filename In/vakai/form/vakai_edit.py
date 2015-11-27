@IN.register('Vakai', type = 'EntityEditForm')
class VakaiEditForm(In.entity.EntityEditForm):
	'''Vakai Edit Form'''
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		#self.id = '-'.join(('vakai', str(self.entity.id), 'edit-form'))
		
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
		# TODO: add cancel button

		self.css.append('ajax i-panel i-panel-box')

@IN.register('VakaiEditForm', type = 'Former')
class VakaiEditFormFormer(In.entity.EntityEditFormFormer):
	'''Vakai Edit Form Former'''
	
	#def submit_prepare(self, form, post):
		
		#super().submit_prepare(form, post)
		
		#if form.has_errors:
			#return
		
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
		
		# no redirect after vakai update
		form.redirect = None
		
		context = IN.context
		
		if not entity:
			context.not_found()
			
		#try:
		
		if context.request.ajax:
			element_id = '-'.join(('.vakai', str(entity.id))) #form.id
			
			# theme children only
			view_mode = 'adminlist'
			# TODO: use parent themed format, view_mode
			themed_entity = IN.themer.theme(entity, view_mode = view_mode)
			
			form.result_commands = [{
				'method' : 'html',
				'args' : [element_id, themed_entity]
			}]
			#output = [{
				#'method' : 'replace',
				#'args' : [element_id, output]
			#}]
			#context.response = In.core.response.CustomResponse(output = output)
		
		else:
			# TODO: dymanic url based on entity view url
			#context.redirect('/'.join((entity.parent_entity_type.lower(), str(entity.parent_entity_id))))
			form.redirect = ''.join(('admin/structure/entity/!', entity.__type, '/bundle/!', entity.type, '/manage/vakai'))
			
				
		#except Exception:
			#IN.logger.debug()

