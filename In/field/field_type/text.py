from In.field.field import Field, FieldFielder, FieldModel


class FieldText(Field):
	__input_field_type__ = 'TextBox'

@IN.register('FieldText', type = 'Fielder')
class FieldTextFielder(FieldFielder):
	'''Base Field Fielder'''


	#field_type = 'Field'


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

		max_allowed = int(field_data.get('max_allowed', 1)) # 0, unlimited
		new_empty_fields = int(field_data.get('new_empty_fields', 1))

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

		for lang, idx_val in field_value.items():
			if lang not in field_languages:

				continue

			for idx, value in idx_val.items():

				name = ''.join((field_name, '[', lang, '][', str(idx), '][value]'))
				id = '_'.join((field_name, lang, str(idx), 'value'))

				input_field_obj = self.get_input_field(self.field_class.__input_field_type__, id, name, value['value'], int(idx), placeholder_text, field_config)
				if input_field_obj:
					obj.add(input_field_obj)

		added = len(obj)
		# add remaining new/empty fields
		if max_allowed != 0:
			new_empty_fields = max_allowed - added
		#print('NEW empty fields', new_empty_fields, ' max ', max_allowed)
		if new_empty_fields > 0:
			# add new empty
			for added_idx in range(added, new_empty_fields + added):
				name = ''.join((field_name, '[', language, '][', str(added_idx), '][value]'))
				id = '_'.join((field_name, language, str(added_idx), 'value'))

				input_field_obj = self.get_input_field(self.field_class.__input_field_type__, id, name, '', added_idx, placeholder_text, field_config)
				if input_field_obj:
					obj.add(input_field_obj)

		return obj

	def get_input_field(self, type, id, name, value, weight, placeholder_text, field_config):
		'''helper method'''

		textfield = Object.new(type, {
			'id' : id,
			'name' : name,
			'value' : value,
			'placeholder' : placeholder_text,
			#'validation_rule' : ['Length', 6, '>', 0, 'The loginname length should be greater than 6.'],
			'css' : ['i-width-1-1 i-form-large'],
			'weight' : weight,
		})

		if field_config['data'].get('field_config', {}).get('required', False):
			textfield.validation_rule = ['Not', [['Empty']], s('{name} is required!', {'name' : field_config['data']['title']})]

		return textfield
