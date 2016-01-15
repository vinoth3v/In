from In.filer import FieldFileFieldFormatter

@IN.register('FieldImage', type = 'FieldFormatter')
class FieldImageFieldFormatter(FieldFileFieldFormatter):
	'''Base class of all IN FieldFormatterBase.

	'''
	
	__info__ = s('image')
	
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
					file_entity_id = idx_value[1]['value']
					if not file_entity_id:
						continue
					values.append(file_entity_id)
					
			output_value = ', '.join(values)
		 
		return output_value
	
	def format_entity(self, field, format, view_mode, args, config):
		
		output_value = ''
		
		display_limit = config.get('display_limit', 0)
		
		link_to_entity = config.get('link_to_entity', False)
		if link_to_entity:
			path = field.entity.path()
			
		field_value_wrapper = config.get('field_value_wrapper', '')
		field_value_wrapper_class = config.get('field_value_wrapper_class', '')
		
		# TODO: view mode based on field config
		field_view_mode = config.get('image_style', view_mode)
		
		field_values = field.value
		
		if field_values is not None:
			values = []
			for lang, lang_value in field_values.items():
				# sort by weight
				si = sorted(lang_value.items(), key = lambda o: int(o[0]))
				added = 0
				for idx_value in si:
					
					# display limit
					if display_limit and added > display_limit:
						break
					
					file_entity_id = int(idx_value[1]['value'])
					
					if not file_entity_id:
						continue
					
					file_entity = IN.entitier.load_single('File', file_entity_id)
					#if file_entity:
						# no use. we manually coding for img tag
						#file_entity.css.append('i-thumbnail i-thumbnail-expand')
						
					themed_file = IN.themer.theme(file_entity, format, field_view_mode)
					
					if field_value_wrapper:
						themed_file = ''.join(('<', field_value_wrapper, ' class="', field_value_wrapper_class, '">', themed_file, '</', field_value_wrapper, '>'))
					
					if link_to_entity:
						
						themed_file = ''.join(('<a href="/', path, '" >', themed_file, '</a>'))
						
					
					values.append(themed_file)
					
					added += 1
					
			output_value = ' '.join(values)
		
		return output_value
