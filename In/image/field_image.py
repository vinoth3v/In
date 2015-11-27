import sys
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
	
	def form_field(self, field_config, field_value = None, language = ''):
		'''returns form field based on field type, data, language'''

		field_name = field_config['field_name']
		field_data = field_config['data']
		
		if field_data is None:
			field_data = {}
		if field_value is None:
			field_value = {}
		
		field_config_data = field_data.get('field_config', {})
		
		title = field_data.get('title', field_name)
		max_limit = int(field_config_data.get('max_limit', 1)) # 0, unlimited
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
			'css' : ['field form-field i-grid']
		})
		
		post = IN.context.request.args['post']
		
		deleted_file_id = 0
		
		if 'ajax_args' in post and 'deleted_file_id' in post['ajax_args']:
			deleted_file_id = int(post['ajax_args']['deleted_file_id'])
			
		added_max_idx = 1
		for lang, idx_val in field_value.items():
			if lang not in field_languages:
				continue
				
			for idx, value in idx_val.items():
				
				name = ''.join((field_name, '[', lang, '][', str(idx), '][value]'))
				id = '_'.join((field_name, lang, str(idx), 'value'))
				#obj.add(self.field_class.__input_field_type__, {
					#'id' : id,
					#'name' : name,
					#'value' : value['value'],
					#'placeholder' : title,
					##'validation_rule' : ['Length', 6, '>', 0, 'The loginname length should be greater than 6.'],
					#'css' : ['i-width-1-1 i-form-large'],
					#'weight' : int(idx),
				#})
				file_entity_id = value['value']
				if not file_entity_id:
					continue
				
				if int(idx) > added_max_idx:
					added_max_idx = int(idx)
				
				#if type(file_entity_id) is list:
					#print('999999999999999999999 LIST ', file_entity_id)
					#for v in file_entity_id:
						#if type(v) is dict:
							#file_entity_id = self.__file_create_from_post__(v)
					
							#if not file_entity_id:
								#continue
				if type(file_entity_id) is dict:
					# process upload
					file_entity_id = self.__file_create_from_post__(file_entity_id)
					
					if not file_entity_id:
						continue
					
					# set the new file value
					value['value'] = file_entity_id
					
				else:
					file_entity_id = int(file_entity_id)
				if not file_entity_id:
					continue
				
				if deleted_file_id == file_entity_id:
					# it is removed
					continue
				
				file_entity = IN.entitier.load_single('File', file_entity_id)
				
				name = ''.join((field_name, '[', lang, '][', str(idx), '][value]'))
				id = '_'.join((field_name, lang, str(idx), 'value'))
				
				themed_file = IN.themer.theme(file_entity, 'html', 'xsmall')
				
				o = obj.add('TextDiv', {
					'id' : id + '-wrapper',
					'value' : themed_file,
					'weight' : int(idx),
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
						#'onclick' : 'jQuery("#'+id+'-wrapper").remove();'
						'data-ajax_partial' : 1,
						'data-ajax_args' : str(file_entity_id).join(('{"deleted_file_id":', '}'))
					},
				})
				
		added = len(obj)
		
		# add remaining new/empty fields
		if max_limit == 0:
			max_limit = sys.maxsize
		
		remaining_fields = max_limit - added
		
		if remaining_fields < new_empty_fields:
			new_empty_fields = new_empty_fields - remaining_fields
		
		if remaining_fields > 0 and new_empty_fields > 0:
			# add new empty
			for added_idx in range(added_max_idx + 1, new_empty_fields + added_max_idx + 1):
				name = ''.join((field_name, '[', language, '][', str(added_idx), '][value]'))
				id = '_'.join((field_name, language, str(added_idx), 'value'))
				
				# TODO: partial elements should be added to ajax_elements to work
				obj.add(self.field_class.__input_field_type__, {
					'id' : id,
					'name' : name,
					'value' : '',
					'title' : s('Select image from disk'),
					'placeholder' : title,
					'css' : ['ajax i-width-1-1 i-form-large'],
					'weight' : added_idx,
					'attributes' : {
						'data-ajax_partial' : 1
					},
				})
		
		return obj


