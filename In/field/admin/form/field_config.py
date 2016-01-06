
#********************************************************************
#					FieldConfig FORM
#********************************************************************	


class FieldConfigFormBase(Form):
	'''Base entity Form class'''
	
	
	
@IN.register('Field', type = 'FieldConfigForm')
class FieldConfigForm(FieldConfigFormBase):
	'''FieldConfig Form'''

	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_name = args['field_name']
		
		set = self.add('FieldSet', {
			'id' : 'titleset',
			'title' : s('Field configuration: {field_name}', {'field_name' : field_name}),
			'css' : ['i-form-row i-margin-large']
		})
		
		# get config data from DB. local cache may be old
		config = IN.fielder.get_enity_bundle_field_config_from_db(entity_type, entity_bundle, field_name)
		config = config[field_name]
		
		field_type = config['field_type']
		config_data = config['data']
		
		field_config = config_data.get('field_config', {})
		
		self.config = config
		admin_path = IN.APP.config.admin_path
		if 'display_config' not in config_data or not config_data['display_config']:
			url = ''.join(('/', admin_path, '/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/display/!default'))
			set.add('TextDiv', {
				'value' : s('After saving this field configuration you should also set the {field display}.', {
					'field display' : ''.join(('<a href="', url, '">', s('field display'), '</a>'))
				})
			})
		
		set.add('TextDiv', {
			'value' : s('Field type : <b>{field_type}</b>', {'field_type' : field_type})
		})
		
		field_title = post.get('title', None)
		if field_title is None: # accept '' as title
			field_title = config_data.get('title', field_name)
			
		set.add('TextBox', {
			'id' : 'title',
			'value' : field_title,
			'title' : s('Field title'),
			'placeholder' : s('Field title'),
			#'validation_rule' : [
			#	'Not', [['Empty', '']], 'The field title is required!'
			#],
			'css' : ['i-width-1-1 i-form-large'],
		})

		set = self.add('FieldSet', {
			'id' : 'configset',
			'css' : ['i-form-row i-margin-large']
		})
		
		# max limit
		set.add('HTMLSelect', {
			'id' : 'max_limit',
			'value' : post.get('max_limit', None) or field_config.get('max_limit', 0),
			'title' : s('Maximum limit'),
			'options' : range(100),
			'required' : True,
			'css' : ['i-form-large'],
			'multiple' : False,
			'info' : s('Maximum number of values allowed on this field. 0 = No limit.'),
			'weight' : 15,
		})
		
		# weight
		set.add('HTMLSelect', {
			'id' : 'weight',
			'value' : post.get('weight', None) or field_config.get('weight', 0),
			'title' : s('Weight'),
			'options' : range(51),
			'required' : True,
			'css' : ['i-form-large'],
			'multiple' : False,
			'info' : s('The order where form field is displayed'),
			'weight' : 15,
		})
		
		set.add('CheckBox', {
			'label' : 'Required?',
			'id' : 'required',
			'value' : 1,	# returned value if checked
			'checked' : post.get('required', 0) == '1' or field_config.get('required', False),
		})
		
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'css' : ['i-form-row i-margin-large'],
			'weight' : 100,
		})

		set.add('Submit', {
			'value' : s('Save settings'),
			'css' : ['i-button i-button-primary']
		})
		set.add('Link', {
			'value' : s('Cancel'),
			'href' : ''.join(('/', admin_path, '/structure/entity/!', entity_type, '/bundle/!', entity_bundle, '/field')),
			'css' : ['i-button']
		})
		
@IN.register('FieldConfigForm', type = 'Former')
class FieldConfigFormFormer(FormFormer):
	'''EntityForm Former'''

	def validate(self, form, post):
		
		if form.has_errors: # fields may have errors
			return
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		
		if form.has_errors:
			return
		
		fielder = IN.fielder
		
		args = form.args
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_name = args['field_name']
		
		# get config data from DB. local cache is old
		config = fielder.get_enity_bundle_field_config_from_db(entity_type, entity_bundle, field_name)
		config = config[field_name]
		config_data = config['data']
		
		# .get(, {}) # no reference if empty
		if 'field_config' not in config_data:
			config_data['field_config'] = {}
			
		field_config = config_data['field_config']
		
		title = form['titleset']['title'].value
		weight = form['configset']['weight'].value
		max_limit = form['configset']['max_limit'].value
		required = post.get('required', 0) == '1'
		
		config_data['title'] = title
		field_config['weight'] = int(weight)
		field_config['max_limit'] = int(max_limit)
		field_config['required'] = required
		
		form.processed_data['config_data'] = config_data
		
		
	def submit(self, form, post):
		'''Save the entity and return entity id'''

		if form.has_errors:
			return
		
		fielder = IN.fielder
		
		args = form.args
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_name = args['field_name']
		
		config_data = form.processed_data['config_data']
		
		try:
			fielder.set_field_config_data(entity_type, entity_bundle, field_name, config_data)
			
		except Exception as e:
			IN.logger.debug()
			form.has_errors = True
			form.error_message = ' '.join((s('Error while saving configuration!'), str(e)))

		


