from collections import OrderedDict
from .text import FieldText, FieldTextFielder
from In.field.field_formatter import FieldFormatter


class FieldTextSelect(FieldText):
	__input_field_type__ = 'HTMLSelect'

@IN.register('FieldTextSelect', type = 'Fielder')
class FieldTextSelectFielder(FieldTextFielder):
	'''Base Field Fielder'''


	def form_field(self, field_config, field_value = None, args = None):
		'''returns form field based on field type, data, language'''

		language = args.get('language', '')

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
		for vals in field_value_options:
			field_options[vals[0]] = vals[1]

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


@IN.register('FieldTextSelect', type = 'FieldFormatter')
class FieldTextSelectFieldFormatter(FieldFormatter):
	'''FieldTextSelect.

	'''

	__info__ = s('Option title')

	def format_value(self, field, format, view_mode, args, config):
		output_value = ''
		texter = IN.texter

		link_to_entity = config.get('link_to_entity', False)
		if link_to_entity:
			path = field.entity.path()

		field_value_wrapper = config.get('field_value_wrapper', '')
		field_value_wrapper_class = config.get('field_value_wrapper_class', '')

		try:
			field_config = IN.fielder.entity_field_config[field.entity_type][field.entity_bundle][field.field_name]['data']['field_config']
		except KeyError as e:
			field_config = {}

		field_value_option_values = field_config.get('field_value_option_values', {})

		field_values = field.value
		if field_values is not None:
			values = []
			for lang, lang_value in field_values.items():
				# sort by weight
				si = sorted(lang_value.items(), key = lambda o: int(o[0]))
				for idx_value in si:

					number = int(idx_value[1]['value'])
					number = field_value_option_values.get(str(number), number)
					text = str(number)

					if link_to_entity:

						text = ''.join(('<a href="/', path, '" >', text, '</a>'))

					if field_value_wrapper:

						text = ''.join(('<', field_value_wrapper, ' class="', field_value_wrapper_class, '">', text, '</', field_value_wrapper, '>'))


					values.append(text)

			output_value = ', '.join(values)

		return output_value

