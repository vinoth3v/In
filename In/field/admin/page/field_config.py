
def field_admin_action_entity_bundle_field_config_form(context, action, entity_type, entity_bundle, field_name, **args):
	
	IN.entitier.access('admin', entity_type, entity_bundle, deny = True)
	
	form_args = {
		'entity_type' : entity_type,
		'entity_bundle' : entity_bundle,
		'field_name' : field_name,
	}
	
	fielder = IN.fielder
	
	field_config = fielder.field_config(entity_type, entity_bundle, field_name)
	
	field_type = field_config['field_type']
	
	field_class = fielder.field_types[field_type]
	config_form = field_class.FieldConfigForm
	
	form = IN.former.load(config_form.__type__, args = form_args)
	
	IN.context.response.output.add(form)
	
