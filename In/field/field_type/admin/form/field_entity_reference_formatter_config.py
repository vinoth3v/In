from In.field.admin.form.field_formatter_config import FieldFormatterConfigForm, FieldFormatterConfigFormFormer


@IN.register('FieldEntityReferenceFieldFormatter', type = 'FieldFormatterConfigForm')
class FieldEntityReferenceFieldFormatterConfigForm(FieldFormatterConfigForm):
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
		
		if 'entity_type' in field_config:
			reference_entity_type = field_config['entity_type']
			reference_entity_bundles = field_config['entity_bundle']
			
			view_modes = IN.entitier.view_modes(reference_entity_type)

			self['configset'].add('HTMLSelect', {
				'id' : 'view_mode',
				'value' : post.get('view_mode', None) or formatter_config.get('view_mode', 'default'),
				'title' : s('View mode'),
				'options' : view_modes,
				'required' : True,
				'multiple' : False,
				'info' : s('Display Referenced entity in this view mode.'),
				'weight' : 1,
			})
			
	
@IN.register('FieldEntityReferenceFieldFormatterConfigForm', type = 'Former')
class FieldEntityReferenceFieldFormatterConfigFormFormer(FieldFormatterConfigFormFormer):
	'''FieldEntityReferenceFieldFormatterConfigForm Former'''

	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		configset = form['configset']
		
		if 'view_mode' in configset:
			
			config = form.processed_data['config']
			
			config['field_formatter_config']['view_mode'] = configset['view_mode'].value
	
