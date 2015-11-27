
def field_admin_action_field_ui_add_field_form(context, action, entity_type, entity_bundle, **args):
	# TODO: admin access

	IN.entitier.access('admin', entity_type, entity_bundle, deny = True)
	
	form_args = {
		'entity_type' : entity_type,
		'entity_bundle' : entity_bundle,
	}
	
	form = IN.former.load('FormFieldAdminAddField', args = form_args)
	IN.context.response.output.add(form)
	
