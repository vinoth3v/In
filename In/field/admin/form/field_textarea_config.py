from collections import OrderedDict

from .field_text_config import FieldTextFieldConfigForm, FieldTextFieldConfigFormFormer

@IN.register('FieldTextArea', type = 'FieldConfigForm')
class FieldTextAreaFieldConfigForm(FieldTextFieldConfigForm):
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
			'value' : post.get('placeholder_text', None) or field_config.get('placeholder_text', ''),
			'title' : s('Placeholder text'),
			'placeholder' : s('Placeholder text'),
			'css' : ['i-width-1-1 i-form-large'],
		})
		
		options = OrderedDict()
		for key in IN.APP.config.ckeditor.keys():
			options[key] = s(key)
			
		set.add('HTMLSelect', {
			'id' : 'ckeditor_config',
			'name' : 'ckeditor_config',
			'title' : s('CKEditor Config'),
			'options' : options,
			'value' : post.get('ckeditor_config', field_config.get('ckeditor_config', '')),
			'multiple' : False,
		})
		
		
@IN.register('FieldTextAreaFieldConfigForm', type = 'Former')
class FieldTextAreaFieldConfigFormFormer(FieldTextFieldConfigFormFormer):
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
		
		field_config['ckeditor_config'] = form['configset']['ckeditor_config'].value
		
		
