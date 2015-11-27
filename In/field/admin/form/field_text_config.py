from In.field.admin.form.field_config import FieldConfigForm, FieldConfigFormFormer

@IN.register('FieldText', type = 'FieldConfigForm')
class FieldTextFieldConfigForm(FieldConfigForm):
	'''FieldTextFieldConfigForm'''

	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_name = args['field_name']
		
		config = self.config
		config_data = config['data']
		field_config = config_data.get('field_config', {})
		
		set = self['configset']
		
		set.add('TextBox', {
			'id' : 'placeholder_text',
			'value' : post.get('placeholder_text', None) or config_data.get('placeholder_text', ''),
			'title' : s('Placeholder text'),
			'placeholder' : s('Placeholder text'),
			'css' : ['i-width-1-1 i-form-large'],
		})
		
		
@IN.register('FieldTextFieldConfigForm', type = 'Former')
class FieldTextFieldConfigFormFormer(FieldConfigFormFormer):
	'''FieldTextFieldConfigForm Former'''
	
	def submit_prepare(self, form, post):
		
		super().submit_prepare(form, post)
		
		if form.has_errors:
			return
		
		args = form.args
		entity_type = args['entity_type']
		entity_bundle = args['entity_bundle']
		field_name = args['field_name']
		
		# get config data from DB. local cache is old
		config_data = form.processed_data['config_data']
		
		field_config = config_data.get('field_config', {})
		
		field_config['placeholder_text'] = form['configset']['placeholder_text'].value
		
		
