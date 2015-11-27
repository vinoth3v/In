
from In.field.admin.form.field_formatter_config import *

#********************************************************************
#					FieldFormatterConfigForm
#********************************************************************	


@IN.register('FieldFileFieldFormatter', type = 'FieldFormatterConfigForm')
class FieldFileFieldFormatterConfigForm(FieldFormatterConfigForm):
	'''Base FieldFormatterConfigForm

	'''

	def __init__(self, data = None, items = None, post = None, **args):

		super().__init__(data, items, post, **args)
		
		field_formatter = args['field_formatter']
		
		display_config = IN.fielder.field_display_config(args['entity_type'], args['entity_bundle'], args['view_mode'], args['field_name'])
		


@IN.register('FieldFileFieldFormatterConfigForm', type = 'Former')
class FieldFileFieldFormatterConfigFormFormer(FieldFormatterConfigFormFormer):
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
		
