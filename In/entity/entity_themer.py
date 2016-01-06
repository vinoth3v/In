

#********************************************************************
#					ENTITY Themer
#********************************************************************


@IN.register('EntityBase', type = 'Themer')
class EntityBaseThemer(In.themer.ObjectThemer):

	theme_tpl_type = 'tpl.py'

	def view_modes(self):
		modes = super().view_modes()
		modes.add('full')
		return modes

	#def theme(self, obj, format, view_mode, args):
		#pass

	#def theme_done(self, obj, format, view_mode, args):
		#pass

	#def theme_items(self, obj, format, view_mode, args):
		#pass

	#def theme_process_variables(self, obj, format, view_mode, args):
		#pass

@IN.register('Entity', type = 'Themer')
class EntityThemer(EntityBaseThemer):


	def view_modes(self):
		modes = super().view_modes()
		modes.add('teaser')
		return modes

	def theme_prepare(self, obj, format, view_mode, args):

		# order the entity fields for this display config, view mode

		# TODO: move to separate function?
		fielder = IN.fielder
		entity_type = obj.__type__
		entity_bundle = obj.type

		if entity_type not in fielder.entity_field_config:
			# entity type not found
			return

		entity_config = fielder.entity_field_config[entity_type]

		if entity_bundle not in entity_config:
			return

		field_config = entity_config[entity_bundle]

		for key, field in field_config.items():

			if key not in obj:
				# field not found in entity
				continue

			field_name = field['field_name']
			default_weight = field['weight']
			weight = default_weight

			display_config = fielder.field_display_config(entity_type, entity_bundle, view_mode, field_name)

			if 'field_formatter_config' in display_config and 'weight' in display_config['field_formatter_config']:
				weight = display_config['field_formatter_config']['weight']

			obj[key].weight = weight

	def theme_attributes(self, obj, format, view_mode, args):
		obj.css.append(obj.__type__)
		obj.css.append('view-mode-' + view_mode)
		obj.css.append('-'.join((obj.__type__, str(obj.id))))
		obj.css.append('-'.join((obj.__type__, obj.type)))
		super().theme_attributes(obj, format, view_mode, args)

	def theme_process_variables(self, obj, format, view_mode, args):
		super().theme_process_variables(obj, format, view_mode, args)

		data = {
			'lazy_args' : {
				'load_args' : {
					'data' : {
						'parent_entity_type' : obj.__type__,
						'parent_entity_id' : obj.id,
						'theme_view_mode' : view_mode
					},
				},
			},
			'parent_entity_type' : obj.__type__,
			'parent_entity_id' : obj.id,
			'weight' : 10,
			'theme_view_mode' : view_mode,
		}

		link = Object.new('EntityContextLinks', data)
		menu = Object.new('EntityContextMenu', data)
		tab = Object.new('EntityContextTab', data)

		theme = IN.themer.theme
		args['entity_context_links'] = theme(link, format, 'lazy')
		args['entity_context_menu'] = theme(menu, format, 'lazy')
		#args['entity_context_tab'] = theme(tab, format, 'lazy')

		if obj.created:
			# lang
			st = obj.created.strftime
			args['created'] = ' '.join((s(st('%B')), st("%d, %Y %I:%M"), s(st('%p'))))

		args['entity_id'] = obj.id
