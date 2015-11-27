
def field_admin_action_entity_bundle_field_field_formatter_form(context, action, entity_type, entity_bundle, view_mode, field_name, **args):
	# TODO: admin access

	IN.entitier.access('admin', entity_type, entity_bundle, deny = True)
	
	output = Object()
	context.response = In.core.response.PartialResponse(output = output)
	
	field_config = IN.fielder.field_config(entity_type, entity_bundle, field_name)
	
	field_type = field_config['field_type']
	
	data = {
		'value' : {},
		'id' : field_name,
		'name' : field_name,
		'entity_type' : entity_type,
		'entity_id' : 0,
	}

	field = Field.new(field_type, data = data)
	
	#config_form = field.FieldFormatter.FieldFormatterConfigForm
	
	args = {
		'entity_type' : entity_type,
		'entity_bundle' : entity_bundle,
		'view_mode' : view_mode,
		'field_type' : field_type,
		'field_name' : field_name,
		'field_config' : field_config,
	}
	
	form = IN.former.load('FieldFormatterSelectionForm', args = args)
	
	#form = IN.former.load(config_form.__type__, args = args)
	element_id = '_'.join((entity_type, entity_bundle, field_name, 'field_formatter_config'))
	o = HTMLObject({
		'id' : element_id,
	})
	
	o.add(form)
	
	context.response.output[element_id] = o
	
	
