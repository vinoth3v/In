from In.field.admin.form.field_formatter_config import FieldFormatterConfigForm, FieldFormatterConfigFormFormer

@IN.register('FieldDateFieldFormatter', type = 'FieldFormatterConfigForm')
class FieldDateFieldFormatterConfigForm(FieldFormatterConfigForm):
	'''FieldDateFieldFormatterConfigForm

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
		
		set = self['configset']
		set.add('TextBox', {
			'id' : 'date_formatter_text',
			'value' : post.get('date_formatter_text', None) or formatter_config.get('date_formatter_text', '%d-%m-%y'),
			'title' : s('Date formatter pattern'),
			'required' : True,
			'multiple' : False,
			'info' : s('date formatter text.'),
			'weight' : 1,
		})
		
	
@IN.register('FieldDateFieldFormatterConfigForm', type = 'Former')
class FieldDateFieldFormatterConfigFormFormer(FieldFormatterConfigFormFormer):
	'''FieldDateFieldFormatterConfigForm Former'''

	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		configset = form['configset']
		
		config = form.processed_data['config']
		
		config['field_formatter_config']['date_formatter_text'] = configset['date_formatter_text'].value
