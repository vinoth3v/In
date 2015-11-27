from .text import FieldText, FieldTextFielder
from In.field.field import FieldModel


class FieldNumber(FieldText):
	__input_field_type__ = 'TextBox'

@IN.register('FieldNumber', type = 'Fielder')
class FieldNumberFielder(FieldTextFielder):
	'''Base Field Fielder'''

	def get_input_field(self, type, id, name, value, weight, placeholder_text, field_config):
		'''helper method'''
		
		inputfield = Object.new(type, {
			'id' : id,
			'name' : name,
			'value' : str(value),
			'placeholder' : placeholder_text,
			'validation_rule' : ['Numeric', 'The field only allows numeric value.'],
			'css' : ['i-width-1-1 i-form-large'],
			'weight' : weight,
		})
		
		if field_config['data'].get('field_config', {}).get('required', False):
			inputfield.validation_rule = ['Not', [['Empty']], s('{name} is required!', {'name' : field_config['data']['title']})]
		
		return inputfield


@IN.register('FieldNumber', type = 'Model')
class FieldNumberModel(FieldModel):

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
		
@IN.hook
def field_model():
	# default model
	return {
		'FieldNumber' : {					# field type
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

