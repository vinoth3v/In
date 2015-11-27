from In.field.field_type.entity_reference import FieldEntityReferenceFieldFormatter

@IN.register('FieldVakai', type = 'FieldFormatter')
class FieldVakaiFieldFormatter(FieldEntityReferenceFieldFormatter):
	'''FieldEntityReference.

	'''
	
	__info__ = s('Vakai')
	
	def format_value(self, field, format, view_mode, args, config):
		return self.format_entity(field, format, view_mode, args, config)
		
	def format_entity(self, field, format, view_mode, args, config):
		
		output_value = ''
		
		entitier = IN.entitier
		
		display_limit = config.get('display_limit', 0)
		
		link_to_entity = config.get('link_to_entity', False)
		if link_to_entity:
			path = field.entity.path()
			
		field_value_wrapper = config.get('field_value_wrapper', '')
		field_value_wrapper_class = config.get('field_value_wrapper_class', '')
		
		if not field_value_wrapper_class:
			field_value_wrapper_class = 'i-subnav i-subnav-line'
			
		field_view_mode = 'tag'
		
		field_values = field.value
		if field_values is not None:
			values = []
			
			for lang, lang_value in field_values.items():
				# sort by weight
				si = sorted(lang_value.items(), key = lambda o: int(o[0]))
				
				added = 0
				
				# TODO: dynamic tag based on configuration
				ul = Object.new('Ul', {
					'css' : [field_value_wrapper_class],
				})
				
				for idx_value in si:
					
					# display limit
					if display_limit and added > display_limit:
						break
					
					vakai_entity_id = idx_value[1]['value']
					
					if not vakai_entity_id:
						continue
					
					vakai_entity = entitier.load_single('Vakai', vakai_entity_id)
						
					entity_title = entitier.entity_title(vakai_entity)
	
					if entity_title:
						
						ul.add('Li', {
							'weight' : added,
						}).add('Link', {
							'value' : entity_title,
							'href' : ''.join(('/vakai', '/!', field.entity.__type__, '/!', field.id, '/', str(vakai_entity.id))),							
						})
					
					added += 1
				
				if len(ul):
					
					# add tag icon
					ul.add('Li', {
						'weight' : -10,
					}).add('TextDiv', {
						'value' : '<i class="i-icon-tags"></i>',
					})
					
					themed_ul = IN.themer.theme(ul)
					values.append(themed_ul)
					
					#themed_vakai = IN.themer.theme(vakai_entity, format, field_view_mode)
					
					#if field_value_wrapper:
						#themed_vakai = ''.join(('<', field_value_wrapper, ' class="', field_value_wrapper_class, '">', themed_vakai, '</', field_value_wrapper, '>'))
					
					#if link_to_entity:						
						#themed_vakai = ''.join(('<a href="/', path, '" class="ajax">', themed_vakai, '</a>'))
					#else:
						#themed_vakai = ''.join(('<a href="/vakai/', str(vakai_entity.id), '" class="ajax">', themed_vakai, '</a>'))
					
			output_value = ''.join(values)
		
		return output_value
