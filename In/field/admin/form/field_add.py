
class FormFieldAdminAddField(Form):

	def __init__(self, data = None, items = None, post = None, **args):

		if data is None: data = {}
		if post is None: post = {}

		if 'id' not in data:
			data['id'] = 'FormFieldAdminAddField'

		super().__init__(data, items, **args)

		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']

		self.entity_type = entity_type
		self.entity_bundle = entity_bundle
		
		self.add('Hidden', {
			'id' : 'entity_type',
			'value' : entity_type,
		})

		self.add('Hidden', {
			'id' : 'entity_bundle',
			'value' : entity_bundle,
		})

		bundle_fields = IN.fielder.bundle_fields(entity_type, entity_bundle)


		set = self.add('FieldSet', {
			'id' : 'addset',
			'title' : s('Add new field'),
			'css' : ['i-form-row i-margin-large']
		})

		field_types = {}
		for field_type, field_class in IN.fielder.field_types.items():
			if field_type != 'Field': # we dont need base fields
				field_types[field_type] = field_class.__type__


		set.add('HTMLSelect', {
			'id' : 'field_type',
			'value' : post.get('field_type', ''),
			'title' : s('New field type'),
			'options' : field_types,
			'required' : True,
			'css' : ['i-width-1-1 i-form-large'],
			'multiple' : False,
		})
		set.add('TextBox', {
			'id' : 'field_name',
			'value' : post.get('field_name', ''),
			'title' : s('New field name'),
			'placeholder' : s('New field name'),
			#'validation_rule' : ['AlphaNum', 'The field name contains invalid values.'],
			'info' : s('Field name can contain only Alphabets, Numbers and underscore.'),
			'css' : ['i-width-1-1 i-form-large'],
		})

		set.add('TextBox', {
			'id' : 'title',
			'value' : post.get('title', ''),
			'title' : s('New field title'),
			'placeholder' : s('New field title'),
			#'validation_rule' : ['AlphaNum', 'The field name contains invalid values.'],
			'info' : s('Field title can contain only Alphabets, Numbers and underscore.'),
			'css' : ['i-width-1-1 i-form-large'],
		})

		#set.add(type = 'HTMLSelect', data = {
			#'id' : 'weight',
			#'value' : post.get('weight', ''),
			#'title' : s('Weight'),
			#'options' : range(50),
			#'required' : True,
			#'css' : ['i-width-1-1 i-form-large']
		#})
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-grid']
		})

		set.add('Submit', {
			'id' : 'submit',
			'value' : s('Add new field'),
			'css' : ['i-button i-button-primary']
		})
		
		admin_path = IN.APP.config.admin_path
		
		set.add('Link', {
			'value' : s('Cancel'),
			'href' : ''.join(('/', admin_path, '/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/field')),
			'css' : ['i-button']
		})
		#set = self.add(type = 'FieldSet', data = {
			#'id' : 'linkset',
			#'css' : ['i-form-row']
		#})

		self.css.append('ajax i-panel i-panel-box i-margin-large')

@IN.register('FormFieldAdminAddField', type = 'Former')
class FormFieldAdminAddFieldFormer(FormFormer):

	def load_arguments(self, form_id, post, args):
		if 'entity_type' in post:
			args['entity_type'] = post['entity_type']
		if 'entity_bundle' in post:
			args['entity_bundle'] = post['entity_bundle']


	def validate(self, form, post):

		if form.has_errors: # fields may have errors
			return

		field_type = form['addset']['field_type'].value
		field_name = form['addset']['field_name'].value

		if not field_type or not field_name:
			form.has_errors = True
			form.error_message = s('Field name cannot be empty!')


	def submit(self, form, post):
		
		if form.has_errors:
			return
			
		entity_type = form.entity_type
		entity_bundle = form.entity_bundle
		addset = form['addset']
		
		field_type = addset['field_type'].value

		field_type = field_type
		
		field_name = addset['field_name'].value
		# always start with field_
		if not field_name.startswith('field_'):
			field_name = 'field_' + field_name
		
		title = addset['title'].value

		weight = 0
		status = 1
		
		data = {
			'title' : title,
		}
		admin_path = IN.APP.config.admin_path
		fielder = IN.fielder
		try:
			created = fielder.__create_new_field__(entity_type, entity_bundle, field_type, field_name, status, weight, data)
			
			if not created:
				# unknown error
				form.has_errors = True
				form.error_message = s('Unknown error occurred while creating new field!')
				return
			
			form.redirect = ''.join((admin_path, '/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/field/!', field_name, '/edit'))
			
		except Exception as e:
			IN.logger.debug()
			form.has_errors = True
			form.error_message = ' '.join((s('Error while creating new field!'), str(e)))

		
