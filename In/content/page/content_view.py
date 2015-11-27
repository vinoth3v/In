
def content_view(context, action, entity_id, **args):

	entity_type = 'Content'
	view_mode = 'full'

	IN.entitier.entity_page_view(entity_type, entity_id, view_mode)
