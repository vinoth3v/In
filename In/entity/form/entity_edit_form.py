import copy

#********************************************************************
#					ENTITY EDIT FORM
#********************************************************************	


class EntityEditFormBase(Form):
	'''Base entity Form class'''
	
	
@IN.register('Entity', type = 'EntityEditForm')
class EntityEditForm(EntityEditFormBase):
	'''Base Entity Edit Form'''


	def __init__(self, data = None, items = None, post = None, **args):
		
		# will raise error if data is none or no entity args
		self.entity_type = data['entity_type']
		self.entity_id = data['entity_id']

		self.entity = IN.entitier.load(self.entity_type, self.entity_id)

		if self.entity is None:
			raise In.html.form.FormException('EntityEditForm: Invalid form arguments!')

		self.entity_bundle = self.entity.type
		
		super().__init__(data, items, **args)
		
		if not post:
			# use entity values
			post = {}
			for field_name, field in self.entity.items():
				post[field_name] = field.value
		
		# add entity bundle fields to this form	
		self.add_entity_bundle_fields(post)
		
		
	def add_entity_bundle_fields(self, field_values = None):
		'''add entity fields to this form'''
		if field_values is None:
			field_values = {}
		fielder = IN.fielder

		# TODO: get fields also by entity language
		bundle_fields = fielder.bundle_fields(self.entity_type, self.entity_bundle)
		for field_name, field_config in bundle_fields.items():

			# TODO: get field value from entity
			field_value = None
			if field_name in field_values:
				field_value = field_values[field_name]
			
			field_element = fielder.form_field(field_config['field_type'], field_config, field_value)
			if field_element is not None:
				
				self.add(field_element)
				try:
					field_element.weight = int(field_config['data']['field_config']['weight'])
				except:
					pass
				
@IN.register('EntityEditForm', type = 'Former')
class EntityEditFormFormer(FormFormer):
	'''EntityEditForm Former'''

	def validate(self, form, post):
		
		if form.has_errors: # fields may have errors
			return

		# form.has_errors = False dont set, field validations may have errors
		
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		# create entity object from form post
		entity_type = form.entity_type
		entity_bundle = form.entity_bundle
		entity_id = int(form.entity_id)
		
		# load old entity
		old_entity = IN.entitier.load(entity_type, entity_id)
		
		edit_entity = copy.deepcopy(old_entity)
		
		ignore = old_entity.Model.not_updatable_columns
		
		for key, value in post.items():
			if key in ignore:
				continue
			if key in edit_entity: # may be it is field
				edit_entity[key] = value
			elif hasattr(edit_entity, key): # attribute
				setattr(edit_entity, key, value)
		
		# object to dict
		edit_dict = edit_entity.__dict__
		
		# update field values
		for key, field in edit_entity.items():
			if isinstance(field, Object):
				edit_dict[key] = field.value
			else:
				edit_dict[key] = field
		
		
		fielder = IN.fielder

		# check/radio boxes may have no keys for fields if no values selected
		# None them
		bundle_fields = fielder.bundle_fields(form.entity_type, form.entity_bundle)
		for field_name, field_config in bundle_fields.items():
			if field_name not in post:
				edit_dict[field_name] = None
		
		## always assign passed types,
		#post['entity_type'] = entity_type
		
		# entity.type is bundle
		post['type'] = entity_bundle
		post['id'] = entity_id

		# set the nabar id
		# TODO: set the nabar id on edit
		# SECURITY: nabar id from post??
		#if 'nabar_id' not in post or not post['nabar_id']:
			#post['nabar_id'] = IN.context.nabar.id
		
		entitier = IN.entitier
		
		entity_class = entitier.types[entity_type]
		edit_entity = entity_class.new(entity_type, edit_dict)
		
		# always set these
		# sub classes can modify it
		edit_entity.id = old_entity.id
		edit_entity.nabar_id = old_entity.nabar_id
		edit_entity.type = old_entity.type
		
		form.processed_data['entity'] = edit_entity
		form.processed_data['old_entity'] = old_entity
		
	def submit(self, form, post):
		'''Save the entity and return entity id'''

		if form.has_errors:
			return
		
		entity_type = form.entity_type
		entity_bundle = form.entity_bundle
		entity_id = int(form.entity_id)
		
		entity = form.processed_data['entity']

		# save the entity
		# override even if id changed in object creation
		entity.id = entity_id
		
		IN.entitier.save(entity)
		
		if entity_id is None:
			# TODO: display error message
			form.has_errors = True
			form.error_message = s('Sorry, Unknown error occurred!')
		else:
			# TODO: dynamic entity urls
			# default redirect to entity page
			form.redirect = entity.path()

