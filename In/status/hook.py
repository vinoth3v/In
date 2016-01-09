

@IN.hook
def access():
	return {
		'status' : {								# group
			'view_status' : {},					# access key
			'view_own_unpublished_status' : {},
			'edit_own_status' : {},
			'edit_own_unpublished_status' : {},
		}
	}
	
@IN.hook
def entity_insert_Status(entity):
	
	# hack
	if hasattr(entity, 'create_comment_container') and not entity.create_comment_container:
		return
	
	IN.commenter.create_comment_container(entity)
