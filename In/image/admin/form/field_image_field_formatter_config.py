from collections import OrderedDict

from In.file.admin.form.field_file_field_formatter_config import FieldFileFieldFormatterConfigForm, FieldFileFieldFormatterConfigFormFormer

#********************************************************************
#					FieldFormatterConfigForm
#********************************************************************	


@IN.register('FieldImageFieldFormatter', type = 'FieldFormatterConfigForm')
class FieldImageFieldFormatterConfigForm(FieldFileFieldFormatterConfigForm):
	'''Base FieldFormatterConfigForm

	'''

	
	
	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		field_formatter = args['field_formatter']
		
		display_config = IN.fielder.field_display_config(args['entity_type'], args['entity_bundle'], args['view_mode'], args['field_name'])
		formatter_config = display_config.get('field_formatter_config', {})
		
		set = self['configset']
		
		options = OrderedDict()
		si = sorted(IN.imager.config_style_filters.keys(), key = lambda o: o)
		for key in si:
			options[key] = key
		
		set.add('HTMLSelect', {
			'id' : 'image_style',
			'title' : s('Image style'),
			'options' : options,
			'required' :  True,
			'value' : post.get('image_style', formatter_config.get('image_style', 'default')),
			'multiple' : False,
		})

@IN.register('FieldImageFieldFormatterConfigForm', type = 'Former')
class FieldImageFieldFormatterConfigFormFormer(FieldFileFieldFormatterConfigFormFormer):
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

		config = form.processed_data['config']
		
		config['field_formatter_config']['image_style'] = form['configset']['image_style'].value
