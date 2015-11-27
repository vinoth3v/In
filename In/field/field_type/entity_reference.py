from In.field.field import Field, FieldFielder, FieldModel
from In.field.field_formatter import FieldFormatter

class FieldEntityReference(Field):
	'''EntityReference field'''
	__input_field_type__ = 'TextBox'
	
	def __init__(self, data = None, items = None, **args):
		super().__init__(data, items, **args)
	
		# check and set to 0 for None, ''
		if self.value:
			for lang, langitems in self.value.items():
				for idx, idxitems in langitems.items():
					if 'value' in idxitems and not idxitems['value']:
						self.value[lang][idx]['value'] = 0
						
@IN.register('FieldEntityReference', type = 'Fielder')
class FieldEntityReferenceFielder(FieldFielder):
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
		max_allowed = int(field_data.get('max_allowed', 1)) # 0, unlimited
		new_empty_fields = int(field_data.get('new_empty_fields', 1))

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
			'css' : ['field form-field'],
			'item_wrapper' : Object.new('TextDiv', {
				'css' : ['field-wrapper']
			})
		})

		for lang, idx_val in field_value.items():
			if lang not in field_languages:
				continue
				
			for idx, value in idx_val.items():
				# TODO
				name = ''.join((field_name, '[', lang, '][', str(idx), '][value]'))
				id = '_'.join((field_name, lang, str(idx), 'value'))
				obj.add(self.field_class.__input_field_type__, {
					'id' : id,
					'name' : name,
					'value' : value['value'],
					'placeholder' : title,
					#'validation_rule' : ['Length', 6, '>', 0, 'The loginname length should be greater than 6.'],
					'css' : ['i-width-1-1 i-form-large'],
					'weight' : int(idx),
				})

		added = len(obj)
		# add remaining new/empty fields
		if max_allowed != 0:
			new_empty_fields = max_allowed - added

		if new_empty_fields > 0:
			# add new empty
			for added_idx in range(added, new_empty_fields + added):
				name = ''.join((field_name, '[', language, '][', str(added_idx), '][value]'))
				id = '_'.join((field_name, language, str(added_idx), 'value'))
				obj.add(self.field_class.__input_field_type__, {
					'id' : id,
					'name' : name,
					'value' : '',
					'placeholder' : title,
					#'validation_rule' : ['Length', 6, '>', 0, 'The loginname length should be greater than 6.'],
					'css' : ['i-width-1-1 i-form-large'],
					'weight' : added_idx,
				})
		
		return obj

	def prepare_insert(self, field):
		'''prepare the field submit values to db insert'''
		
		value = field.value
		entity = field.entity
		entitier = IN.entitier
		
		if value:
			for lang, lang_items in value.items():
				for idx, idx_items in lang_items.items():
					field_value = idx_items['value']
					if not field_value:
						idx_items['value'] = 0
						
@IN.register('FieldEntityReference', type = 'Model')
class FieldEntityReferenceModel(FieldModel):

	def __create_field_table__(self, field_name):

		'''Creates table in DB for this field'''
		field_type = self.field_type
		table = IN.fielder.field_table(field_name)
		q = ['CREATE TABLE IF NOT EXISTS ']
		q.append(table)
		q.append(''' (
			id bigserial PRIMARY KEY,
			entity_type character varying(64),
			entity_id bigint,
			language character varying(5),
			weight smallint,
			value bigint,
			created timestamp without time zone,
			status smallint DEFAULT 1			
		);''')

		## index
		#q.append('CREATE INDEX ')

		#index_name = table.split('.')[-1]

		#q.append(index_name + '_idx ')
		
		#q.append(' ON ' + table)
		#q.append(' USING btree ')
		#q.append(''' (
			#entity_type,
			#entity_id,
			#weight
		#);''')

		IN.db.execute(''.join(q))

		# caller will commit
	
	

@IN.register('FieldEntityReference', type = 'FieldFormatter')
class FieldEntityReferenceFieldFormatter(FieldFormatter):
	'''FieldEntityReference.

	'''
	
	__info__ = s('Entity')
	
	def format_value(self, field, format, view_mode, args, config):
		return self.format_entity(field, format, view_mode, args, config)
		
	def format_entity_id(self, field, format, view_mode, args, config):
		output_value = ''
		
		field_values = field.value
		if field_values is not None:
			values = []
			for lang, lang_value in field_values.items():
				# sort by weight
				si = sorted(lang_value.items(), key = lambda o: int(o[0]))
				for idx_value in si:
					entity_id = idx_value[1]['value']
					if not entity_id:
						continue
					values.append(entity_id)
					
			output_value = ', '.join(values)
		 
		return output_value
	
	def format_entity(self, field, format, view_mode, args, config):
		
		output_value = ''
		try:
			field_config = IN.fielder.entity_field_config[field.entity_type][field.entity_bundle][field.field_name]['data']['field_config']
		except KeyError as e:
			field_config = {}
			
		if 'entity_type' not in field_config:
			return ''
		
		field_entity_type = field_config['entity_type']			
		field_view_mode = config.get('view_mode', view_mode)
		
		field_values = field.value
		if field_values is not None:
			values = []
			for lang, lang_value in field_values.items():
				
				si = sorted(lang_value.items(), key = lambda o: int(o[0])) # sort by weight
				
				for idx_value in si:
					entity_id = idx_value[1]['value']
					if not entity_id:
						continue
					
					entity = IN.entitier.load_single(field_entity_type, entity_id)
					if not entity:
						continue
					
					themed_output = IN.themer.theme(entity, format, field_view_mode)
					values.append(themed_output)

			output_value = ' '.join(values)
		
		return output_value



@IN.hook
def field_model():
	# default model
	return {
		'FieldEntityReference' : {					# field type
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

