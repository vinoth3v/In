from collections import OrderedDict

#********************************************************************
#					FieldFormatterConfigForm
#********************************************************************	


class FieldFormatterConfigFormBase(Form):
	'''Base entity Form class'''
	
	
	
@IN.register('FieldFormatter', type = 'FieldFormatterConfigForm')
class FieldFormatterConfigForm(FieldFormatterConfigFormBase):
	'''Base FieldFormatterConfigForm

	'''


	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, **args)
		
		field_formatter = args['field_formatter']
		
		fielder = IN.fielder
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_name = args['field_name']
		view_mode = args['view_mode']
		
		config = fielder.field_config(entity_type, entity_bundle, field_name)
		
		field_config_data = config.get('data', {})
		field_config = field_config_data.get('field_config', {})
		
		display_config = fielder.field_display_config(entity_type, entity_bundle, view_mode, field_name)
		
		formatter_config = display_config.get('field_formatter_config', {})
		
		set = self.add('FieldSet', {
			'id' : 'titleset',
			'css' : ['i-form-row i-margin-large']
		})
		
		# TODO: element ids conflict with multiple formatter config on same form
		
		options = OrderedDict()
		options['hidden'] = s('Hidden')
		options['label'] = s('Label')
		options['h1'] = s('h1')
		options['h2'] = s('h2')
		options['h3'] = s('h3')
		options['h4'] = s('h4')
		
		set.add('HTMLSelect', {
			'id' : 'field_title',
			'title' : s('Field title'),
			'options' : options,
			'required' :  True,
			'value' : post.get('field_title', formatter_config.get('title', 'label')),
			'multiple' : False,
		})
		
		set = self.add('FieldSet', {
			'id' : 'configset',
			'title' : 'Config ' + field_formatter,
			'css' : ['i-form-row i-margin-large']
		})
		
		#max_limit = field_config.get('max_limit', 0)
		
		#if max_limit != 1: # max limit is input limit
			
		set.add('HTMLSelect', {
			'id' : 'display_limit',
			'title' : s('Display limit'),
			'options' : range(0, 101),
			'required' :  True,
			'value' : int(post.get('display_limit', formatter_config.get('display_limit', 0))),
			'multiple' : False,
			'info' : s('How many field values should display? 0 : unlimited'),
		})
		
		options = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'label', 'b', 'strong', 'i', 'em', 'strike', 'big', 'small', 'mark', 'div', 'span', 'p', 'center', 'pre', 'code', 'blockquote', 'q', 'address', 'ul', 'ol', 'li']
		
		set.add('HTMLSelect', {
			'id' : 'field_value_wrapper',
			'title' : s('Field value wrapper'),
			'options' : options,
			'required' :  False,
			'value' : post.get('field_value_wrapper', formatter_config.get('field_value_wrapper', '')),
			'multiple' : False,
		})
		
		set.add('TextBox', {
			'id' : 'field_value_wrapper_class',
			'title' : s('Field value wrapper css classes'),
			'required' :  False,
			'value' : post.get('field_value_wrapper_class', formatter_config.get('field_value_wrapper_class', '')),
			'css' : ['i-width-1-1']
		})
		
		set.add('CheckBox', {
			'label' : 'Link to entity?',
			'id' : 'link_to_entity',
			'value' : 1,	# returned value if checked
			'checked' : post.get('link_to_entity', 0) == '1' or formatter_config.get('link_to_entity', False),
		})
		
		
		# weight
		set.add('HTMLSelect', {
			'id' : 'weight',
			'value' : int(post.get('weight', None) or formatter_config.get('weight', 0)),
			'title' : s('Weight'),
			'options' : range(51),
			'required' : True,
			'css' : [''],
			'multiple' : False,
			'info' : s('The order where form field is displayed'),
			'weight' : 15,
		})
		
		
		set = self.add('FieldSet', {
			'id' : 'actionset',
			'title' : '',
			'css' : ['i-form-row i-margin-large']
		})

		set.add('Submit', {
			'value' : s('Save settings'),
			'css' : ['i-button i-button-primary']
		})
		

@IN.register('FieldFormatterConfigForm', type = 'Former')
class FieldFormatterConfigFormFormer(FormFormer):
	'''FieldFormatterConfigForm Former'''

	def validate(self, form, post):
		
		if form.has_errors:
			return
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		args = form.args
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		view_mode = args['view_mode']
		field_name = args['field_name']
		field_formatter = args['field_formatter']
		
		title = form['titleset']['field_title'].value

		config = {
			'field_formatter' : field_formatter,
			'field_formatter_config' : {
				'title' : title,
			},
		}
		
		configset = form['configset']
		
		if 'display_limit' in form['configset']:
			config['field_formatter_config']['display_limit'] = int(configset['display_limit'].value)
		
		config['field_formatter_config']['link_to_entity'] = post.get('link_to_entity', 0) == '1'
		
		config['field_formatter_config']['field_value_wrapper'] = configset['field_value_wrapper'].value
		config['field_formatter_config']['field_value_wrapper_class'] = configset['field_value_wrapper_class'].value
		
		config['field_formatter_config']['weight'] = int(configset['weight'].value)
		
		config['field_formatter_config']['display_limit'] = int(configset['display_limit'].value)
		
		form.processed_data['config'] = config
		
	def submit(self, form, post):
		'''Save the entity and return entity id'''

		if form.has_errors:
			return
		
		args = form.args
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		view_mode = args['view_mode']
		field_name = args['field_name']
		
		config = form.processed_data['config']
		
		try:
			IN.fielder.set_field_formatter_config(entity_type, entity_bundle, view_mode, field_name, config)
		except Exception as e:
			IN.logger.debug()
			form.has_errors = True
			form.error_message = ' '.join((s('Error while updating display configuration!'), str(e)))




@IN.register('DefaultStringFieldFormatter', type = 'FieldFormatterConfigForm')
class DefaultStringFieldFormatterConfigForm(FieldFormatterConfigForm):
	'''FieldEntityReferenceFieldFormatterConfigForm

	'''
	
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		field_formatter = args['field_formatter']
		
		fielder = IN.fielder
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_name = args['field_name']
		view_mode = args['view_mode']
		
		config = fielder.field_config(entity_type, entity_bundle, field_name)
		
		field_config_data = config.get('data', {})
		field_config = field_config_data.get('field_config', {})
		
		display_config = fielder.field_display_config(entity_type, entity_bundle, view_mode, field_name)
		
		formatter_config = display_config.get('field_formatter_config', {})
		
		
		# TODO: element ids conflict with multiple formatter config on same form
		
		options = {}
		for style in IN.APP.config.texter.keys():
			options[style] = style
			
		self['configset'].add('HTMLSelect', {
			'id' : 'texter_style',
			'title' : s('Texter style'),
			'options' : options,
			'required' :  True,
			'value' : post.get('texter_style', formatter_config.get('texter_style', 'default')),
			'multiple' : False,
		})
		
@IN.register('DefaultStringFieldFormatterConfigForm', type = 'Former')
class DefaultStringFieldFormatterConfigFormFormer(FieldFormatterConfigFormFormer):
	'''DefaultStringFieldFormatterConfigForm Former'''
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		configset = form['configset']
		
		if 'texter_style' in configset:
			
			config = form.processed_data['config']
			
			config['field_formatter_config']['texter_style'] = configset['texter_style'].value
			
