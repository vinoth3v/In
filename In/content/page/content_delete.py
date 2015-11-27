
def content_entity_delete_form(context, action, entity_id, **args):

	entity_type = 'Content'

	entitier = IN.entitier

	entity_id = int(entity_id)
	
	IN.entitier.entity_page_delete(entity_type, entity_id)
