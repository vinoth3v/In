from collections import OrderedDict

from In.field import FieldEntityReference, FieldEntityReferenceFielder

class FieldVakai(FieldEntityReference):
	'''FieldVakai field'''
	#__input_field_type__ = 'FileUpload'

@IN.register('FieldVakai', type = 'Fielder')
class FieldVakaiFielder(FieldEntityReferenceFielder):
	'''FieldVakai Fielder'''

	default_file_bundle = 'image'

	def form_field(self, field_config, field_value = None, args = None):
		'''returns form field based on field type, data, language'''

		language = args.get('language', '')


		# add selectize
		asset = IN.context.asset
		# TODO: selectize CSS not working some time
		asset.add_css('/files/libraries/selectize.js/dist/css/selectize.css', 'selectize.css')

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
		new_empty_fields = int(data_field_config.get('new_empty_fields', 1))

		vakai_bundle = data_field_config.get('vakai_bundle', 'vakai')

		field_selection_type = data_field_config.get('field_selection_type', 'autocomplete')


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
			'css' : ['field form-field']
		})

		# get field values
		field_values = []

		for lang, idx_val in field_value.items():
			if lang not in field_languages:

				continue

			for idx, value in idx_val.items():

				self.__get_vakais_from_post__(value, field_values, vakai_bundle)

		# get field options
		field_options = OrderedDict()
		if field_selection_type != 'autocomplete':
			# we need options only for non auto complete field types
			# TODO: ORDER BY weight/title
			entities = IN.entitier.load_all_by_bundle('Vakai', vakai_bundle)

			if entities:
				si = sorted(entities.values(), key = lambda o: o.weight)
				for vakai in si:
					title_field_name = vakai.Entitier.title_field_name
					field_options[vakai.id] = vakai[title_field_name].value[''][0]['value']
		else:
			# we need options only for non auto complete field types
			entities = IN.entitier.load_multiple('Vakai', field_values)

			if entities:
				si = sorted(entities.values(), key = lambda o: o.weight)
				for vakai in si:
					title_field_name = vakai.Entitier.title_field_name
					try:
						field_options[vakai.id] = vakai[title_field_name].value[''][0]['value']
					except Exception as e1:
						field_options[vakai.id] = 'NOT FOUND'

		# TODO: get language
		lang = ''
		name = ''.join((field_name, '[', lang, '][0][value]'))
		id = '_'.join((field_name, lang, 'value'))

		if field_selection_type == 'autocomplete':
			o = obj.add('HTMLSelect', {
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
			o = obj.add('HTMLSelect', {
				'id' : id,
				'name' : name,
				'value' : field_values,
				'options' : field_options,
				'css' : ['i-width-1-1'],
			})
		elif field_selection_type == 'checkboxes':
			o = obj.add('CheckBoxes', {
				'id' : id,
				'name' : name,
				'value' : field_values,
				'options' : field_options,
				'css' : ['i-width-1-1'],
			})
		elif field_selection_type == 'radioboxes':
			if field_values:
				field_values = field_values[0]

			o = obj.add('RadioBoxes', {
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

	def __prepare_inset_update__(self, field):
		'''prepare the field submit values to db insert/update'''
		'''prepare the field submit values to db update'''

		field_value = field.value

		if not field_value:
			return


		entity = field.entity
		entitier = IN.entitier
		vakaigal = IN.vakaigal
		fielder = IN.fielder


		bundle_fields = fielder.bundle_fields(entity.__type__, entity.type)

		config = bundle_fields[field.name]

		config_data = config.get('data', {})
		data_field_config = config_data.get('field_config', {})
		vakai_bundle = data_field_config.get('vakai_bundle', 'vakai')


		field_languages = ['']

		entitier = IN.entitier

		for lang, idx_val in field_value.items():
			if lang not in field_languages:
				continue

			new_values = []

			for idx, value in idx_val.items():

				self.__get_vakais_from_post__(value, new_values, vakai_bundle)

			field_value[lang] = {} # reset for this lang
			if new_values:
				idx = 0
				for v in new_values:
					field_value[lang][idx] = {
						'value' : v
					}

					idx = idx + 1


		# update newly added values

	def prepare_insert(self, field):
		'''prepare the field submit values to db insert'''
		self.__prepare_inset_update__(field)

	def prepare_update(self, field):
		'''prepare the field submit values to db update'''
		self.__prepare_inset_update__(field)

	def __get_vakais_from_post__(self, values, ids, vakai_bundle):

		entitier = IN.entitier
		vakaigal = IN.vakaigal


		if type(values) is int:
			ids.append(values)
			return

		if type(values) is str:

			if values.isnumeric():

				ids.append(int(values))
				return

			# check if title exists
			entity = vakaigal.find_by_title(values, vakai_bundle)
			if entity:

				ids.append(entity.id)
				return

			# create new vakai if field allowed
			#title_field_name = vakai.Entitier.title_field_name
			values = values.strip()

			if not values:
				return

			data = {
				'type' : vakai_bundle,
				'field_vakai_title' : {
					'': {
						0: {
							'value': values
						}
					}
				},
				'weight' : 0
			}

			try:
				entity_class = entitier.types['Vakai']
				entity = entity_class.new('Vakai', data)

				entity.save()

				ids.append(entity.id)
				return

			except Exception as e:
				IN.logger.debug()

			return

		if type(values) is dict:
			if 'value' in values:
				v = values['value']
				self.__get_vakais_from_post__(v, ids, vakai_bundle)

			return

		if type(values) is list:
			for v in values:
				self.__get_vakais_from_post__(v, ids, vakai_bundle)


