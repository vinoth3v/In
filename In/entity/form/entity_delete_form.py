
#********************************************************************
#					ENTITY DELETE FORM
#********************************************************************	


class EntityDeleteFormBase(Form):
	'''Base entity Delete Form class'''
	
@IN.register('Entity', type = 'EntityDeleteForm')
class EntityDeleteForm(EntityDeleteFormBase):
	'''Base Entity Edit Form'''


	def __init__(self, data = None, items = None, post = None, **args):
		
		# will raise error if data is none or no entity args
		self.args = args
		entitier = IN.entitier

		self.entity = entitier.load(args['entity_type'], args['entity_id'])

		if self.entity is None:
			raise In.html.form.FormException('EntityDeleteForm: Invalid form arguments!')
		
		title = entitier.entity_title(self.entity) or ''
		
		title = text = IN.texter.format(title, 'default')
		
		self.add('TextDiv', {
			'value' : s('Are you sure you want to delete {title}?', {'title' : title})
		})
		
		super().__init__(data, items, **args)
		
@IN.register('EntityDeleteForm', type = 'Former')
class EntityDeleteFormFormer(FormFormer):
	'''EntityDeleteForm Former'''

	def validate(self, form, post):
		
		if form.has_errors:
			return
			
		# access check
		if not IN.entitier.access('delete', form.entity):
			form.has_errors = True
			form.error_message = s('You have no permission to do this action!')
		
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
			
	def submit(self, form, post):
		'''Delete the entity'''

		if form.has_errors:
			return
		
		# no default implementation
		# we should call explicitly call IN.entitier.delete in sub classes
		
		## create entity object from form post
		#entity_type = form.entity_type
		#entity_bundle = form.entity_bundle
		#entity_id = int(form.entity_id)

		## always assign passed types,
		#post['entity_type'] = entity_type
		## entity.type is bundle
		#post['type'] = entity_bundle
		#post['id'] = entity_id

		#entitier = IN.entitier
		
		#entity_class = entitier.types[entity_type]
		#entity = entity_class.new(entity_type, post)

		## save the entity
		## override even if id changed in object creation
		#entity.id = entity_id
		
		#entitier.save(entity)
		
		#if entity_id is None:
			## TODO: display error message
			#form.has_errors = True
			#form.error_message = s('Sorry, Unknown error occurred!')
		#else:
			## default redirect to entity page
			#form.redirect = '/'.join((entity_type.lower(), str(entity_id)))

