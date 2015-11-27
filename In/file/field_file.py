import os
import shutil
import json

from In.field import Field, FieldFielder
from In.field import FieldEntityReference, FieldEntityReferenceFielder
from In.field import FieldFormatter, FieldFormatterConfigForm

import magic

class FieldFile(FieldEntityReference):
	'''EntityReference field'''
	__input_field_type__ = 'FileUpload'
	
@IN.register('FieldFile', type = 'Fielder')
class FieldFileFielder(FieldEntityReferenceFielder):
	'''Base Field Fielder'''

	default_file_bundle = 'file'
	
	#def form_field(self, field_config, field_value = None, language = ''):
		#'''returns form field based on field type, data, language'''

		#field_name = field_config['field_name']
		#field_data = field_config['data']
		#if field_data is None:
			#field_data = {}
		#if field_value is None:
			#field_value = {}
		#print(field_value)
		#title = field_data.get('title', field_name)
		#max_allowed = int(field_data.get('max_allowed', 1)) # 0, unlimited
		#new_empty_fields = int(field_data.get('new_empty_fields', 1))

		## '': field is available to all language
		#field_languages = field_data.get('languages', [''])
		#if field_languages is None:
			#field_languages = [''] # all language

		## return if field is not for this language
		#if language not in field_languages:
			#return
		
		## wrapper
		#obj = Object.new('HTMLField', {
			#'id' : field_name,
			#'title' : title,
			#'weight': field_config['weight'],
			#'css' : ['field form-field']
		#})

		#for lang, idx_val in field_value.items():
			#if lang not in field_languages:
				#continue
				
			#for idx, value in idx_val.items():
				## TODO
				#name = ''.join((field_name, '[', lang, '][', str(idx), '][value]'))
				#id = '_'.join((field_name, lang, str(idx), 'value'))
				#obj.add(type = self.field_class.__input_field_type__, data = {
					#'id' : id,
					#'name' : name,
					#'value' : value['value'],
					#'placeholder' : title,
					##'validation_rule' : ['Length', 6, '>', 0, 'The loginname length should be greater than 6.'],
					#'css' : ['i-width-1-1 i-form-large'],
					#'weight' : int(idx),
				#})

		#added = len(obj)
		## add remaining new/empty fields
		#if max_allowed != 0:
			#new_empty_fields = max_allowed - added

		#if new_empty_fields > 0:
			## add new empty
			#for added_idx in range(added, new_empty_fields + added):
				#name = ''.join((field_name, '[', language, '][', str(added_idx), '][value]'))
				#id = '_'.join((field_name, language, str(added_idx), 'value'))
				#obj.add(type = self.field_class.__input_field_type__, data = {
					#'id' : id,
					#'name' : name,
					#'value' : '',
					#'placeholder' : title,
					##'validation_rule' : ['Length', 6, '>', 0, 'The loginname length should be greater than 6.'],
					#'css' : ['i-width-1-1 i-form-large'],
					#'weight' : added_idx,
				#})
		
		#return obj
	
	def __file_create_from_post__(self, field_value):
		if type(field_value) is not dict:
			return int(field_value)
		
		if '__upload__' in field_value and field_value['__upload__'] and field_value['path']:
			
			path = field_value['path']
			
			# invalid?
			if not os.path.exists(path):
				IN.logger.debug(path + ' not exists')
				return
			
			size = os.path.getsize(path)
			
			# returns bytes
			mime = magic.from_file(path, mime=True).decode("utf-8")
			mime1, mime2 = mime.split('/', 1)
			
			public_file_dir = IN.APP.config.public_file_dir
			
			save_to = 'images/' + str(IN.context.nabar.id)
			
			save_to = os.path.join(public_file_dir, save_to)						
			
			# create folder
			os.makedirs(save_to, exist_ok = True)
			file_name = os.path.split(path)[1]
			save_to = os.path.join(save_to, file_name)
			
			shutil.move(path, save_to)
			
			path = save_to
			
			# TODO: strip the path prefix
			
			path = path.replace(public_file_dir + '/', '', 1)
			
			# create new File entity
			file = Entity.new('File', {
				'type' : self.default_file_bundle,
				'nabar_id' : IN.context.nabar.id,	# current user
				'status' : 1,			# active
				'path' : path,
				'size' : size,
				'mime1' : mime1,
				'mime2' : mime2,
				'remote': 0,
				'data'	: json.dumps({}, skipkeys = True, ensure_ascii = False),
			})
			file_id = IN.entitier.save(file)
			
			return file_id
		
	def __field_prepare_insert_update__(self, field):
		'''prepare the field submit values to db insert/update'''
	
		value = field.value
		entity = field.entity
		entitier = IN.entitier
		
		if value:
			for lang, lang_items in value.items():
				for idx, idx_items in lang_items.items():
					field_value = idx_items['value']
					# new file uploaded
					
					if type(field_value) is dict and '__upload__' in field_value and field_value['__upload__'] and field_value['path']:
						
						file_id = self.__file_create_from_post__(field_value)
						
						if file_id:
							field.value[lang][idx]['value'] = file_id
						else:
							
							raise Exception('Unable to save the file ' + field_value['path'])
							IN.logger.debug('Unable to save the file ' + field_value['path'])
							#del field.value[lang][idx]
							field.value[lang][idx]['value'] = 0
							continue
		
	
	def prepare_insert(self, field):
		'''prepare the field submit values to db insert'''
		self.__field_prepare_insert_update__(field)
		
	def prepare_update(self, field):
		'''prepare the field submit values to db update'''
		self.__field_prepare_insert_update__(field)
		

@IN.hook
def field_model():
	# default model
	return {
		'FieldFile' : {					# field type
			'columns' : {							# table columns
				'id' : {'type' : 'bigserial'},
				'entity_type' : {'type' : 'varchar', 'length' : 64},
				'entity_id' : {'type' : 'bigint'},
				'language' : {'type' : 'varchar', 'length' :  4, 'default' : 'lang'},
				'weight' : {'type' : 'smallint'},
				'value' : {'type' : 'bigint'}, 		# big int
				'created' : {},
			},
			'keys' : {
				'primary' : 'id',
			},
		},
	}

#class (Field):
	#__input_field_type__ = 'TextBox'

#@IN.register('FieldFile', type = 'Fielder')
#class (FieldFielder):
	#'''Base Field Fielder'''


	#def form_field(self, field_config, field_value = None, language = ''):
		#'''returns form field based on field type, data, language'''

		#print('FFFFFFFFFFFFFFFF', field_value)
		#field_name = field_config['field_name']
		#field_data = field_config['data']
		#if field_data is None:
			#field_data = {}
		#if field_value is None:
			#field_value = {}
		#print('f1f1f1f1', field_value)
		#title = field_data.get('title', field_name)
		#max_allowed = int(field_data.get('max_allowed', 1)) # 0, unlimited
		#new_empty_fields = int(field_data.get('new_empty_fields', 1))
		#print(max_allowed, new_empty_fields)
		## '': field is available to all language
		#field_languages = field_data.get('languages', [''])
		#if field_languages is None:
			#field_languages = [''] # all language

		## return if field is not for this language
		#if language not in field_languages:
			#print('LLLLLLLLLL this field is not available in language', field_name, language, field_languages)
			#return
		
		## wrapper
		#obj = Object.new('HTMLField', {
			#'id' : field_name,
			#'title' : title,
			#'weight': field_config['weight'],
			#'css' : ['field form-field']
		#})
		#print('field name obj', obj.id)
		#for lang, idx_val in field_value.items():
			#if lang not in field_languages:
				#print('lang not avai', lang, idx_val)
				#continue
				
			#for idx, value in idx_val.items():

				#name = ''.join((field_name, '[', lang, '][', str(idx), '][value]'))
				#id = '_'.join((field_name, lang, str(idx), 'value'))
				#obj.add(type = self.field_class.__input_field_type__, data = {
					#'id' : id,
					#'name' : name,
					#'value' : value['value'],
					#'placeholder' : title,
					##'validation_rule' : ['Length', 6, '>', 0, 'The loginname length should be greater than 6.'],
					#'css' : ['i-width-1-1 i-form-large'],
					#'weight' : int(idx),
				#})

		#added = len(obj)
		## add remaining new/empty fields
		#if max_allowed != 0:
			#new_empty_fields = max_allowed - added
		#print('NEW empty fields', new_empty_fields, ' max ', max_allowed)
		#if new_empty_fields > 0:
			## add new empty
			#for added_idx in range(added, new_empty_fields + added):
				#name = ''.join((field_name, '[', language, '][', str(added_idx), '][value]'))
				#id = '_'.join((field_name, language, str(added_idx), 'value'))
				#obj.add(type = self.field_class.__input_field_type__, data = {
					#'id' : id,
					#'name' : name,
					#'value' : '',
					#'placeholder' : title,
					##'validation_rule' : ['Length', 6, '>', 0, 'The loginname length should be greater than 6.'],
					#'css' : ['i-width-1-1 i-form-large'],
					#'weight' : added_idx,
				#})
		
		#return obj
		


@IN.register('FieldFile', type = 'FieldFormatter')
class FieldFileFieldFormatter(FieldFormatter):
	'''Base class of all IN FieldFormatterBase.

	'''
	
	__info__ = s('file')
	
	def format_value(self, field, format, view_mode, args, config):
		output_value = ''
		
		
		field_values = field.value
		if field_values is not None:
			values = []
			for lang, lang_value in field_values.items():
				# sort by weight
				si = sorted(lang_value.items(), key = lambda o: int(o[0]))
				for idx_value in si:
					values.append(str(idx_value[1]['value']))
					
			output_value = ', '.join(values)
		
		return output_value


