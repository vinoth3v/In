def status_add_form(context, action, entity_bundle, **args):

	entitier = IN.entitier
	entity_type = 'Status'

	# access denied
	entitier.access('add', entity_type, entity_bundle, deny = True)
		

	form = entitier.get_entity_add_form(entity_type, entity_bundle)

	if form is not None:
		context.response.output.add(form)
	
	
