
def content_entity_add_form(context, action, entity_bundle, **args):

	entitier = IN.entitier
	entity_type = 'Content'

	# access denied
	entitier.access('add', entity_type, entity_bundle, deny = True)
	
	context.page_title = s('Add {bundle} content', {'bundle' : s(entity_bundle)})
	
	form = entitier.get_entity_add_form(entity_type, entity_bundle)

	if form is not None:
		context.response.output.add(form)
