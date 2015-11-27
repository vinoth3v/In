from In.core.object_meta import ObjectMetaBase


class FieldFormatterMeta(ObjectMeta):

	__class_type_base_name__ = 'FieldFormatterBase'
	__class_type_name__ = 'FieldFormatter'


class FieldFormatterBase(Object, metaclass = FieldFormatterMeta):
	'''Base class of all IN FieldFormatterBase.

	'''
	__allowed_children__ = None
	__default_child__ = None

	__info__ = s('base FieldFormatter')

	def format(self, field, format, view_mode, args, config):
		'''format the field and return as text.'''
		return ''
		

	
@IN.register('FieldFormatter', type = 'FieldFormatter')
class FieldFormatter(FieldFormatterBase):
	'''Base class of all IN FieldFormatterBase.

	'''
	
	def format_title(self, field, format, view_mode, args, config):
		
		title_format = config.get('title', 'label')
		if title_format == 'hidden':
			return ''
		return ''.join(('<', title_format, ' class="field-title">', s(field.title), '</', title_format, '>'))
		
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


@IN.register('Field', type = 'FieldFormatter')
class HiddenFieldFormatter(FieldFormatter):
	'''Hide the field.'''
	
	__info__ = s('hide this field')
	
	def format_value(self, field, format, view_mode, args, config):
		return ''

@IN.register('FieldText', type = 'FieldFormatter')
class DefaultStringFieldFormatter(FieldFormatter):
	'''Base class of all IN FieldFormatterBase.

	'''
	
	__info__ = s('plain text')
	
	def format_value(self, field, format, view_mode, args, config):
		output_value = ''
		texter = IN.texter
		
		texter_style = config.get('texter_style', 'default')
		
		link_to_entity = config.get('link_to_entity', False)
		if link_to_entity:
			path = field.entity.path()
			
		field_value_wrapper = config.get('field_value_wrapper', '')
		field_value_wrapper_class = config.get('field_value_wrapper_class', '')
		
		field_values = field.value
		if field_values is not None:
			values = []
			for lang, lang_value in field_values.items():
				# sort by weight
				si = sorted(lang_value.items(), key = lambda o: int(o[0]))
				for idx_value in si:
					text = str(idx_value[1]['value'])
					text = texter.format(text, texter_style)
					
					if link_to_entity:
						
						text = ''.join(('<a href="/', path, '" >', text, '</a>'))
					
					if field_value_wrapper:
						
						text = ''.join(('<', field_value_wrapper, ' class="', field_value_wrapper_class, '">', text, '</', field_value_wrapper, '>'))
					
					
					values.append(text)
					
			output_value = ', '.join(values)
		
		return output_value

