from collections import OrderedDict
from .text_select import FieldTextSelect, FieldTextSelectFielder

from In.field.field_formatter import FieldFormatter

class FieldNumberSelect(FieldTextSelect):
	__input_field_type__ = 'HTMLSelect'

@IN.register('FieldNumberSelect', type = 'Fielder')
class FieldNumberSelectFielder(FieldTextSelectFielder):
	'''Base Field Fielder'''


	def form_field(self, field_config, field_value = None, language = ''):
		'''returns form field based on field type, data, language'''
		
		field_name = field_config['field_name']
		field_data = field_config['data']
		if field_data is None:
			field_data = {}
		if field_value is None:
			field_value = {}
		
		title = s(field_data.get('title', field_name))
		
		data_field_config = field_data.get('field_config', {})
		placeholder_text = data_field_config.get('placeholder_text', '')

		max_limit = int(data_field_config.get('max_limit', 1)) # 0, unlimited
		
		
		field_value_options = data_field_config.get('field_value_options', [])
		
		# to keep order and easy lookup
		field_value_options_keys = data_field_config.get('field_value_option_keys', [])
		field_value_option_values = data_field_config.get('field_value_option_values', {})
		
		
		new_empty_fields = int(data_field_config.get('new_empty_fields', 1))
		
		field_selection_type = data_field_config.get('field_selection_type', 'select')
		
		
		# '': field is available to all language
		field_languages = field_data.get('languages', [''])
		if field_languages is None:
			field_languages = [''] # all language

		# return if field is not for this language
		if language not in field_languages:
			#print('this field is not available in language', field_name, language, field_languages)
			return
		
		# wrapper
		obj = Object.new('HTMLField', {
			'id' : field_name,
			'title' : title,
			'weight': field_config['weight'],
			'css' : ['field form-field'],
			'item_wrapper' : Object.new('TextDiv', {
				'css' : ['field-wrapper']
			})
		})
		
		# get field values
		field_values = []
		
		for lang, lang_val in field_value.items():
			if lang not in field_languages:
				continue
			for idx, idx_val in lang_val.items():
				field_values.append(str(idx_val['value'])) # values only match by str
		

		# get field options
		field_options = OrderedDict()
		for val in field_value_options_keys:
			field_options[val] = field_value_option_values[val]
		
		
		# TODO: get language
		lang = ''
		name = ''.join((field_name, '[', lang, '][0][value]'))
		id = '_'.join((field_name, lang, 'value'))
		
		#print('max_limit', max_limit)
		
		if field_selection_type == 'autocomplete':
			obj.add('HTMLSelect', {
				'id' : id,
				'name' : name,
				'value' : field_values,
				'options' : field_options,
				'css' : ['autocomplete i-width-1-1'],
				'multiple' : max_limit > 1,
				'attributes' : {
					#'multiple' :  if : None,	# TODO: dynamic
					'data-autocomplete_max_items' : max_limit,
					'data-autocomplete_create' : '1',
					'data-autocomplete_url' : vakai_bundle.join(('/vakai/!', '/autocomplete')),
					#'data-autocomplete_options' : init_options,
				}
			})
		elif field_selection_type == 'select':
			if max_limit == 1 and field_values:
				field_values = field_values[0]
			
			obj.add('HTMLSelect', {
				'id' : id,
				'name' : name,
				'value' : field_values,
				'options' : field_options,
				'css' : ['i-width-1-1'],			
				'multiple' : True if max_limit == 0 or max_limit > 1 else False,
				'required' : data_field_config.get('required', False)
			})
		elif field_selection_type == 'checkboxes':
			if max_limit == 1 and field_values:
				field_values = field_values[0]
			
			obj.add('CheckBoxes', {
				'id' : id,
				'name' : name,
				'value' : field_values,
				'options' : field_options,
				'css' : ['i-width-1-1'],
			})
		elif field_selection_type == 'radioboxes':
			if field_values:
				field_values = field_values[0]
			else:
				field_values = None
			obj.add('RadioBoxes', {
				'id' : id,
				'name' : name,
				'value' : field_values,
				'options' : field_options,
				'css' : ['i-width-1-1'],
			})
		else:
			# TODO: other module may handle this?
			pass
		
		return obj


