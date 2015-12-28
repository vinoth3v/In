import sys, json
from In.field import Field, FieldFielder
from In.file import FieldFile, FieldFileFielder
from In.file import FieldFileFieldFormatterConfigForm, FieldFileFieldFormatterConfigFormFormer

class FieldImage(FieldFile):
	'''EntityReference field'''
	__input_field_type__ = 'FileUpload'

@IN.register('FieldImage', type = 'Fielder')
class FieldImageFielder(FieldFileFielder):
	'''FieldImage Fielder'''

	default_file_bundle = 'image'

	def form_field(self, field_config, field_value = None, args = None):
		'''returns form field based on field type, data, language'''

		form = args['form']
		language = args.get('language', '')

		field_name = field_config['field_name']
		field_data = field_config['data']

		if field_data is None:
			field_data = {}
		if field_value is None:
			field_value = {}

		field_config_data = field_data.get('field_config', {})
		placeholder_text = field_config_data.get('placeholder_text', '')
		
		title = field_data.get('title', field_name)
		max_limit = int(field_config_data.get('max_limit', 1)) # 0, unlimited
		
		if max_limit == 0:
			max_limit = sys.maxsize


		new_empty_fields = int(field_config_data.get('new_empty_fields', 1))

		# '': field is available to all language
		field_languages = field_data.get('languages', [''])
		if field_languages is None:
			field_languages = [''] # all language

		# return if field is not for this language
		if language not in field_languages:
			return

		# wrapper
		obj = Object.new('HTMLField', {
			'id' : field_name,
			'title' : title,
			'weight': field_config['weight'],
			'css' : ['field form-field']
		})
		
		grid = obj.add('TextDiv', {
			'css' : ['i-container']
		}).add('TextDiv', {
			'css' : ['i-grid']
		})

		# ajax replaceable
		form.ajax_elements.append(field_name)

		post = IN.context.request.args['post']
		
		deleted_file_id = 0

		if 'ajax_args' in post and 'deleted_file_id' in post['ajax_args']:
			deleted_file_id = int(post['ajax_args']['deleted_file_id'])
		
		entitier = IN.entitier
		themer = IN.themer
		
		added_max_idx = 1
		for lang, idx_val in field_value.items():
			if lang not in field_languages:
				continue
			
			new_idx = 0
			
			for idx in sorted(idx_val.keys(), key = lambda o:o):
				
				value = idx_val[idx]
				
				file_entity_id = value['value']
				if not file_entity_id:
					continue

				ids = []
				
				if type(file_entity_id) is dict:
					# process upload
					file_entity_id = self.__file_create_from_post__(file_entity_id)

					if not file_entity_id:
						continue

					# set the new file value
					value['value'] = file_entity_id
					
					ids = [file_entity_id]
					
				elif type(file_entity_id) is list: # multiple values from browser
					ids = file_entity_id
				else:
					file_entity_id = int(file_entity_id)
					ids = [file_entity_id]
					
				if not ids:
					continue
				
				for file_entity_id in ids:
					
					if deleted_file_id == file_entity_id:
						# it is removed
						continue
					
					file_entity = entitier.load_single('File', file_entity_id)

					name = ''.join((field_name, '[', lang, '][', str(new_idx), '][value]'))
					id = '_'.join((field_name, lang, str(new_idx), 'value'))

					themed_file = themer.theme(file_entity, 'html', 'xsmall')

					o = grid.add('TextDiv', {
						'id' : id + '-wrapper',
						'value' : themed_file,
						'weight' : int(new_idx),
						'css' : ['i-thumbnail']
					})
					o.add('Hidden', {
						'id' : id,
						'name' : name,
						'value' : str(file_entity_id)
					})
					o.add('TextDiv', {
						'value' : '<i class="i-icon-close"></i>',
						'css' : ['ajax i-pointer i-thumbnail-caption'],
						'attributes' : {
							'data-ajax_partial' : 1,
							'data-ajax_args' : str(file_entity_id).join(('{"deleted_file_id":', '}'))
						},
					})
					
					if new_idx >= max_limit - 1:
						break
					
					new_idx += 1
					
		
		added_max_idx = new_idx
		
		added = len(grid)

		# add remaining new/empty fields

		remaining_fields = max_limit - added

		if remaining_fields < new_empty_fields:
			new_empty_fields = new_empty_fields - remaining_fields

		if remaining_fields > 0 and new_empty_fields > 0:
			# add new empty
			for added_idx in range(added_max_idx + 1, new_empty_fields + added_max_idx + 1):
				name = ''.join((field_name, '[', language, '][', str(added_idx), '][value]'))
				id = '_'.join((field_name, language, str(added_idx), 'value'))

				input_field_obj = self.get_input_field(self.field_class.__input_field_type__, id, name, '', added_idx, placeholder_text, field_config, args)
				if input_field_obj:
					obj.add(input_field_obj)

		return obj
		
	def get_input_field(self, type, id, name, value, weight, placeholder_text, field_config, form_args):
		'''helper method'''
		
		input_field = Object.new(type, {
			'id' : id,
			'name' : name,
			'value' : '',
			'title' : s('Select image from disk'),
			'placeholder' : placeholder_text,
			'css' : ['ajax i-width-1-1 i-form-large'],
			'weight' : weight,
			'attributes' : {
				'data-ajax_partial' : 1
			},
		})
		
		if field_config['data'].get('field_config', {}).get('required', False):
			input_field.validation_rule = ['Not', [['Empty']], s('{name} is required!', {'name' : field_config['data']['title']})]
		
		return input_field



class FieldImageBrowser(FieldImage):
	'''Image browser and upload field'''
	__input_field_type__ = 'FileUpload'

@IN.register('FieldImageBrowser', type = 'Fielder')
class FieldImageBrowserFielder(FieldImageFielder):
	'''FieldImage Fielder'''
	
	def get_input_field(self, type, id, name, value, weight, placeholder_text, field_config, form_args = None):
		'''helper method'''
		
		form = form_args['form']
		input_field = Object.new('TextDiv', {
			'id' : id + '_button',
			'name' : name + '_button',
			'value' : s('Select image'),
			'css' : ['i-button ajax-modal'],
			'weight' : weight,
			'attributes' : {
				'data-href' : '/field/image/browse',
				'data-modal_class' : 'i-modal-dialog-large',
				'data-modal_options' : '{center:true}',
				'data-ajax_args' : json.dumps({
					'field_id' : id,
					'field_name' : name,
					'form_id' : form.id,
				}, skipkeys = True, ensure_ascii = False)
			},
		})
		
		input_field.add('HTMLSelect', {
			'id' : id,
			'name' : name,
			'options' : {},
			'css' : ['ajax i-hidden'],
			'attributes' : {
				'data-ajax_partial' : 1
			},
		})
		
		return input_field