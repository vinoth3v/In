
import datetime

from .text import FieldText, FieldTextFielder
from In.field.field import FieldModel
from In.field.field_formatter import FieldFormatter


class FieldDate(FieldText):
	__input_field_type__ = 'DateSelect'

@IN.register('FieldDate', type = 'Fielder')
class FieldDateFielder(FieldTextFielder):
	'''Base Field Fielder'''


	def prepare_insert(self, field):
		'''prepare the field submit values to insert'''
		
		self.prepare_insert_update(field)
	
	def prepare_update(self, field):
		
		self.prepare_insert_update(field)
		
	def prepare_insert_update(self, field):
		'''prepare the field submit values to update'''
		
		if not field.value:
			return
		for lang, lang_vals in field.value.items():
			for idx, idx_vals in lang_vals.items():
				value = idx_vals['value']
				
				if isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
					continue
				
				if 'year' not in value and 'month' not in value:
					idx_vals['value'] = None
				else:
					year = int(value['year']) if 'year' in value else datetime.datetime.now().year
					month = int(value['month']) if 'month' in value else 1
					day = int(value['day']) if 'day' in value else 1
					idx_vals['value'] = datetime.datetime(year, month, day)
					


@IN.register('FieldDate', type = 'Model')
class FieldDateModel(FieldModel):

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
			value timestamp without time zone,
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
		'FieldDate' : {					# field type
			'columns' : {							# table columns
				'id' : {'type' : 'bigserial'},
				'entity_type' : {'type' : 'varchar', 'length' : 64},
				'entity_id' : {'type' : 'bigint'},
				'language' : {'type' : 'varchar', 'length' :  4, 'default' : 'lang'},
				'weight' : {'type' : 'smallint'},
				'value' : {'type' : 'timestamp'}, 		# big int
				'created' : {},
			},
			'keys' : {
				'primary' : 'id',
			},
		},
	}


@IN.register('FieldDate', type = 'FieldFormatter')
class FieldDateFieldFormatter(FieldFormatter):
	'''FieldDate.

	'''
	
	__info__ = s('Date')
	
	def format_value(self, field, format, view_mode, args, config):
		output_value = ''
		texter = IN.texter
		
		
		link_to_entity = config.get('link_to_entity', False)
		if link_to_entity:
			path = field.entity.path()
			
		field_value_wrapper = config.get('field_value_wrapper', '')
		field_value_wrapper_class = config.get('field_value_wrapper_class', '')
		
		date_formatter_text = config.get('date_formatter_text', '%d-%m-%Y')
		
		field_values = field.value
		if field_values is not None:
			values = []
			for lang, lang_value in field_values.items():
				# sort by weight
				si = sorted(lang_value.items(), key = lambda o: int(o[0]))
				for idx_value in si:
					
					datetime = idx_value[1]['value']
					text = datetime.strftime(date_formatter_text)
					
					if link_to_entity:
						
						text = ''.join(('<a href="/', path, '" >', text, '</a>'))
					
					if field_value_wrapper:
						
						text = ''.join(('<', field_value_wrapper, ' class="', field_value_wrapper_class, '">', text, '</', field_value_wrapper, '>'))
					
					values.append(text)
					
			output_value = ', '.join(values)
		
		return output_value

