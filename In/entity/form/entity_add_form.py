
#********************************************************************
#					ENTITY ADD FORM
#********************************************************************


class EntityAddFormBase(Form):
	'''Base entity Form class'''


@IN.register('Entity', type = 'EntityAddForm')
class EntityAddForm(EntityAddFormBase):
	'''Base Entity Form

	Entity form instance should be per bundle.
	'''

	def __init__(self, data = None, items = None, post = None, **args):

		# after submit it may have value
		self.entity_id = None

		# will raise error if data is none or no entity args

		self.entity_type = data['entity_type']
		self.entity_bundle = data['entity_bundle']

		# moved to Form, default
		#self.args = args

		super().__init__(data, items, **args)

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

			args = {
				'form' : self
			}
			field_element = fielder.form_field(field_config['field_type'], field_config, field_value, args)
			if field_element is not None:

				self.add(field_element)

				try:
					field_element.weight = int(field_config['data']['field_config']['weight'])
				except:
					pass

		#for i, t in self.items():
			#print(i, t.weight)

@IN.register('EntityAddForm', type = 'Former')
class EntityAddFormFormer(FormFormer):
	'''EntityForm Former'''

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

		# always assign passed types,
		post['entity_type'] = entity_type
		# entity.type is bundle
		post['type'] = entity_bundle

		# make use of form args
		post.update(form.args)

		entitier = IN.entitier

		entity_class = entitier.types[entity_type]
		entity = entity_class.new(entity_type, post)

		form.processed_data['entity'] = entity

		if entity.nabar_id == 0:
			entity.nabar_id = IN.context.nabar.id


	def submit(self, form, post):
		'''Save the entity and return entity id'''

		if form.has_errors:
			return

		entity_type = form.entity_type
		entity_bundle = form.entity_bundle

		entitier = IN.entitier

		entity = form.processed_data['entity']

		# save the entity
		entity_id = entitier.save(entity)

		if entity_id is None:
			# TODO: display error message
			form.has_errors = True
			form.error_message = s('Sorry, Unknown error occurred!')
		else:
			# set the new entity_id
			form.entity_id = entity_id
			# default redirect to entity page
			form.redirect = entity.path()


